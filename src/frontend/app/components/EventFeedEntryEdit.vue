<template>
  <UForm :schema="bottleFeedSchema" :state="state" class="flex flex-col justify-between gap-10 h-full"
    @submit="onSubmit">
    <div class="h-full flex flex-col gap-5">

      <!-- Amount -->
      <div class="flex flex-col  gap-3">
        <div class="flex flex-row justify-between w-full">
          <label class="font-bold">Amount</label>
          <span class="opacity-80">{{ state.amountMl }}ml ({{ mlToOz(state.amountMl, 1) }}oz)</span>
        </div>

        <UFormField name="amountMl">
          <USlider v-model="state.amountMl" size="xl" :min="0" :max="200" />
        </UFormField>
      </div>

      <!-- Time -->
      <UFormField name="time">
        <div class="flex flex-col gap-3">
          <label class="font-bold">Time</label>

          <UInput v-model="state.time" size="xl" type="time" :default-value="state.time" />
        </div>
      </UFormField>

      <!-- Type -->
      <UFormField name="isFormula">

        <div class="flex flex-col gap-3">


          <label class="font-bold">Feed Type</label>

          <URadioGroup size="xl" variant="card" v-model="state.isFormula" :items="isFormulaItems"
            orientation="horizontal" indicator="hidden" :ui="{
              fieldset: 'flex flex-row items-center justify-between md:justify-start w-full',
              item: 'flex-grow'
            }">
            <template #label="{ item }">
              <div class="flex flex-row items-center gap-1">
                <UIcon v-if="item.icon" class="text-2xl" :name="item.icon" />
                <span>{{ item.label }}</span>
              </div>
            </template>
          </URadioGroup>
        </div>
      </UFormField>
    </div>
    <UButton size="xl" block type="submit">Log Bottle Feed</UButton>
  </UForm>
</template>

<script lang="ts" setup>
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types';
import * as v from 'valibot'
import type { FormSubmitEvent, RadioGroupItem } from '@nuxt/ui';
defineEmits<{
  submit: [],
  cancel: []
}>()

const props = withDefaults(defineProps<{
  feedEvent?: IAPIBottleFeedEvent
}>(), {
  feedEvent: undefined
})

const toast = useToast()

const isLoading = ref(false)

const eventStore = useEventStore()

const { $api } = useNuxtApp()

const startingFeedData: IAPIBottleFeedEvent = props.feedEvent ? props.feedEvent : await eventStore.getDefaultBottleFeedEventData();

const bottleFeedSchema = v.object({
  amountMl: v.pipe(v.number()),
  time: v.pipe(v.string()),
  date: v.pipe(v.date()),
  isFormula: v.pipe(v.boolean())
})

type BottleFeedSchema = v.InferOutput<typeof bottleFeedSchema>

const state: BottleFeedSchema = reactive({
  amountMl: startingFeedData.amount_ml,
  date: new Date(),
  time: dateToLocalTimeString(new Date()),
  isFormula: startingFeedData.is_formula
})

const isFormulaItems = ref<RadioGroupItem[]>([
  {
    label: "Formula",
    icon: "i-mdi-pot-mix",
    // @ts-expect-error Using a boolean here seems to work fine, and matches the API.
    value: true,
  },
  {
    label: "Breast Milk",
    icon: "i-healthicons-breast-pump",
    // @ts-expect-error Using a boolean here seems to work fine, and matches the API.
    value: false
  }
])

async function onSubmit(event: FormSubmitEvent<BottleFeedSchema>) {

  isLoading.value = true

  try {
    // Split the "HH:MM" string
    const [hours, minutes] = event.data.time.split(":").map(Number);

    if (!hours) throw new Error("Hours is unexpectedly undefined.")

    // Clone the date to avoid mutating original
    const combinedDate = new Date(event.data.date);

    // Set the hours/minutes on that date
    combinedDate.setHours(hours, minutes, 0, 0);

    // Format as ISO string for the API
    const timeStart: string = combinedDate.toISOString();

    const newBottleFeed: IAPIBottleFeedEvent = {
      name: "feed_bottle",
      description: "",
      id: "",
      amount_ml: event.data.amountMl,
      is_formula: event.data.isFormula,
      time_start: timeStart
    }

    await $api.feed.createEventBottleFeed(newBottleFeed)

    eventStore.clearEditState()

    toast.add({
      title: "Feed Event Logged",
      color: "success",
    })

  } catch (e) {

    console.error("Error creating new bottle feed event", e)

  } finally {
    isLoading.value = false
  }

}
</script>

<style></style>