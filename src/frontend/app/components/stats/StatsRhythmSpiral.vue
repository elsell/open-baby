<template>
  <div class="rhythm-spiral-container">
    <div ref="chartContainer" class="chart-wrapper" />
    <div ref="tooltip" class="tooltip" role="tooltip" />
  </div>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'

/* Props */
interface FeedData {
  time: string
  amount_ml: number
  time_since_last_feed_minutes: number
}

const props = defineProps<{
  feedData: FeedData[] | null | undefined
  // accept a reactive "isDark" boolean (page passes useColorMode() computed)
  isDark?: boolean | null | undefined
}>()

/* Refs */
const chartContainer = ref<HTMLDivElement | null>(null)
const tooltip = ref<HTMLDivElement | null>(null)
let svg: d3.Selection<SVGGElement, unknown, null, undefined> | null = null
let resizeObserver: ResizeObserver | null = null

/* Helper: normalize input and ensure sorted ascending */
const normalized = computed(() => {
  const rows = props.feedData ?? []
  return rows
    .map((r) => ({
      ...r,
      // keep original time string but parse ms for sorting/scale
      timeMs: Number.isFinite(Number(r.time)) ? Number(r.time) : Date.parse(r.time)
    }))
    .filter((r) => Number.isFinite(r.timeMs))
    .sort((a, b) => a.timeMs - b.timeMs)
})

/* Tooltip text formatting */
const formatFeedTime = (iso: string) => {
  const d = new Date(iso)
  return `${d.toLocaleDateString()}, ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
}

const renderChart = async () => {
  if (!chartContainer.value) return
  // wait a tick so layout is stable (helps when component mounts during SSR hydration)
  await nextTick()

  const data = normalized.value
  // clear previous
  d3.select(chartContainer.value).select('svg').remove()
  if (!data.length) return

  const width = chartContainer.value.clientWidth
  if (width <= 0) return
  const height = width
  const margin = Math.max(12, width * 0.05)
  const maxRadius = Math.min(width, height) / 2 - margin

  const startDate = new Date(data[0].time)
  const endDate = new Date(data[data.length - 1].time)

  // svg container
  svg = d3
    .select(chartContainer.value)
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .attr('viewBox', `0 0 ${width} ${height}`)
    .append('g')
    .attr('transform', `translate(${width / 2}, ${height / 2})`)

  // tooltip element
  const tipEl = tooltip.value
  if (!tipEl) return
  const tip = d3.select<HTMLDivElement, unknown>(tipEl)

  // scales
  const timeToAngle = d3
    .scaleLinear()
    .domain([0, 24 * 3600 * 1000])
    .range([0, 2 * Math.PI])

  const timeToRadius = d3.scaleTime<Date, number>().domain([startDate, endDate]).range([20, maxRadius])

  // amount extent + fallback
  const amountExtent = d3.extent(data, (d) => d.amount_ml as number)
  let minAmt = amountExtent[0] ?? 0
  let maxAmt = amountExtent[1] ?? Math.max(1, minAmt + 1)
  if (minAmt === maxAmt) {
    maxAmt = minAmt + 1
    minAmt = Math.max(0, minAmt - 1)
  }
  const amountToSize = d3.scaleSqrt().domain([minAmt, maxAmt]).range([2, Math.max(6, width * 0.014)])

  // interval color scale (map the actual extent -> interpolateTurbo)
  const intervalExtent = d3.extent(data, (d) => d.time_since_last_feed_minutes as number)
  let intervalMin = intervalExtent[0] ?? 0
  let intervalMax = intervalExtent[1] ?? Math.max(1, intervalMin + 1)
  if (intervalMin === intervalMax) intervalMax = intervalMin + 1
  const intervalToColor = d3.scaleSequential(d3.interpolateTurbo).domain([intervalMin, intervalMax])

  // choose neutral stroke/text colors from prop
  const spiralStroke = props.isDark ? '#9ca3af' : '#444'
  const markerStroke = props.isDark ? '#6b7280' : '#555'
  const markerText = props.isDark ? '#e6eef8' : '#888'
  const tooltipBg = getComputedStyle(chartContainer.value).getPropertyValue('--tooltip-bg') || (props.isDark ? 'rgba(0,0,0,0.75)' : 'rgba(45,45,45,0.9)')
  const tooltipText = getComputedStyle(chartContainer.value).getPropertyValue('--tooltip-text') || (props.isDark ? '#fff' : '#fff')

  // spiral path
  const spiralPoints = d3.timeMinutes(startDate, endDate, 30).map((dt) => {
    const timeOfDayMs = (dt.getHours() * 3600 + dt.getMinutes() * 60 + dt.getSeconds()) * 1000
    const angle = timeToAngle(timeOfDayMs) - Math.PI / 2
    const radius = timeToRadius(dt)
    return { x: radius * Math.cos(angle), y: radius * Math.sin(angle) }
  })

  svg
    .append('path')
    .datum(spiralPoints)
    .attr('class', 'spiral-path')
    .attr('d', d3.line<{ x: number; y: number }>().x((d) => d.x).y((d) => d.y) as any)
    .attr('stroke', spiralStroke)

  // time markers
  const timeMarkers = [
    { label: '12 AM', angle: -Math.PI / 2 },
    { label: '6 AM', angle: 0 },
    { label: '12 PM', angle: Math.PI / 2 },
    { label: '6 PM', angle: Math.PI }
  ]

  timeMarkers.forEach((marker) => {
    svg
      .append('line')
      .attr('class', 'time-marker-line')
      .attr('x1', 0)
      .attr('y1', 0)
      .attr('x2', maxRadius * Math.cos(marker.angle))
      .attr('y2', maxRadius * Math.sin(marker.angle))
      .attr('stroke', markerStroke)

    svg
      .append('text')
      .attr('class', 'time-marker-label')
      .attr('x', (maxRadius + width * 0.02) * Math.cos(marker.angle))
      .attr('y', (maxRadius + width * 0.02) * Math.sin(marker.angle))
      .attr('dy', '0.35em')
      .attr('fill', markerText)
      .style('font-size', Math.max(10, width * 0.02) + 'px')
      .attr('text-anchor', 'middle')
      .text(marker.label)
  })

  // draw events
  const events = svg
    .selectAll('circle.feed')
    .data(data.filter((d) => d.time_since_last_feed_minutes > 0))
    .join('circle')
    .attr('class', 'feed')
    .attr('cx', (d) => {
      const dt = new Date(d.time)
      const tp = timeToAngle((dt.getHours() * 3600 + dt.getMinutes() * 60 + dt.getSeconds()) * 1000)
      return timeToRadius(dt) * Math.cos(tp - Math.PI / 2)
    })
    .attr('cy', (d) => {
      const dt = new Date(d.time)
      const tp = timeToAngle((dt.getHours() * 3600 + dt.getMinutes() * 60 + dt.getSeconds()) * 1000)
      return timeToRadius(dt) * Math.sin(tp - Math.PI / 2)
    })
    .attr('r', (d) => amountToSize(d.amount_ml))
    .style('fill', (d) => intervalToColor(d.time_since_last_feed_minutes))
    .style('stroke', 'transparent')
    .style('cursor', 'pointer')

  // events: mouse handlers (use event.currentTarget to avoid `this` ambiguity)
  events
    .on('mouseover', (event, d) => {
      d3.select(event.currentTarget as SVGCircleElement)
        .transition()
        .duration(100)
        .attr('r', amountToSize(d.amount_ml) * 1.5)
        .style('stroke', '#ffffff')

      tip
        .style('visibility', 'visible')
        .style('background', tooltipBg)
        .style('color', tooltipText)
        .html(`
          <div class="tooltip-time">${formatFeedTime(d.time)}</div>
          <div class="tooltip-detail">
            Amount: <strong>${d.amount_ml} ml</strong><br>
            Time Since Last: <strong>${d.time_since_last_feed_minutes.toFixed(1)} min</strong>
            (${(d.time_since_last_feed_minutes / 60).toFixed(2)} hrs)
          </div>
        `)
    })
    .on('mousemove', (event) => {
      tip.style('top', `${(event as MouseEvent).pageY + 12}px`).style('left', `${(event as MouseEvent).pageX + 12}px`)
    })
    .on('mouseout', (event, d) => {
      d3.select(event.currentTarget as SVGCircleElement)
        .transition()
        .duration(200)
        .attr('r', amountToSize(d.amount_ml))
        .style('stroke', 'transparent')

      tip.style('visibility', 'hidden')
    })
}

/* watchers & lifecycle: re-render on data or theme change, keep responsive */
watch([() => props.feedData, () => props.isDark], () => {
  // re-render when data or theme toggles
  renderChart()
})

onMounted(() => {
  renderChart()
  // responsive
  resizeObserver = new ResizeObserver(() => {
    renderChart()
  })
  if (chartContainer.value) resizeObserver.observe(chartContainer.value)
})

onUnmounted(() => {
  if (resizeObserver && chartContainer.value) resizeObserver.unobserve(chartContainer.value)
})
</script>

<style scoped>
.rhythm-spiral-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.chart-wrapper {
  width: 100%;
  max-width: 800px;
  min-height: 220px;
}

/* tooltip is positioned absolutely relative to page (page container must not clamp it). */
.tooltip {
  position: absolute;
  visibility: hidden;
  background: var(--tooltip-bg, rgba(45, 45, 45, 0.9));
  color: var(--tooltip-text, #fff);
  border-radius: 8px;
  padding: 10px;
  font-size: 0.9rem;
  pointer-events: none;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
  max-width: 260px;
  text-align: left;
}

/* D3 elements: rely on inline stroke/fill set by the component so scoping is safe */
.spiral-path {
  stroke-width: 1px;
  stroke-dasharray: 2 4;
  fill: none;
}

.time-marker-line {
  stroke-width: 1px;
}

.time-marker-label {
  font-size: 0.75rem;
  text-anchor: middle;
}
</style>
