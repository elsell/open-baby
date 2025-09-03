<template>
  <UForm
:schema="bottleFeedSchema" :state="state" class="flex flex-col justify-between gap-10 h-full"
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
      <div class="flex flex-row gap-5">
        <UFormField name="date">
          <div class="flex flex-col gap-3">
            <label class="font-bold">Date</label>

            <UInput v-model="state.date" size="xl" type="date" />
          </div>
        </UFormField>
        <UFormField name="time">
          <div class="flex flex-col gap-3">
            <label class="font-bold">Time</label>

            <UInput v-model="state.time" size="xl" type="time" :default-value="state.time" />
          </div>
        </UFormField>
      </div>

      <!-- Type -->
      <UFormField name="isFormula">

        <div class="flex flex-col gap-3">


          <label class="font-bold">Feed Type</label>

          <URadioGroup
            v-model="state.isFormula"
            size="xl" variant="card" :items="isFormulaItems"
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
    <UButton size="xl" block type="submit" :loading="isLoading">
      {{ isEdit ? 'Edit Bottle Feed' : 'Log Bottle Feed' }}
    </UButton>
    {{ state }}
  </UForm>
</template>

<script lang="ts" setup>
import type { IAPIBottleFeedEvent } from '~~/repository/modules/feed/types';
import * as v from 'valibot'
import type { RadioGroupItem } from '@nuxt/ui';
import { useEventForm } from '~/composables/useEventForm';

const emit = defineEmits<{
  submit: [],
  cancel: []
}>()

const props = withDefaults(defineProps<{
  feedEvent?: IAPIBottleFeedEvent
  isEdit?: boolean
}>(), {
  feedEvent: undefined
})

const { $api } = useNuxtApp()
const eventStore = useEventStore();

const bottleFeedSchema = v.object({
  amountMl: v.pipe(v.number()),
  time: v.pipe(v.string()),
  date: v.pipe(v.string()),
  isFormula: v.pipe(v.boolean()),
  notes: v.nullish(v.pipe(v.string()))
})

type BottleFeedSchema = v.InferOutput<typeof bottleFeedSchema>

const startingFeedData = props.feedEvent ? props.feedEvent : await eventStore.getDefaultBottleFeedEventData();

const initialState: BottleFeedSchema = {
  amountMl: startingFeedData.amount_ml,
  date: '', // Will be set by the composable
  time: '', // Will be set by the composable
  isFormula: startingFeedData.is_formula,
  notes: props.isEdit ? startingFeedData.notes : undefined
};

const { state, onSubmit, isLoading } = useEventForm<typeof bottleFeedSchema, IAPIBottleFeedEvent>({
  schema: bottleFeedSchema,
  createEvent: (data) => $api.events.feed.createEventBottleFeed({
    ...data,
    name: 'feed_bottle',
    description: '',
    amount_ml: data.amountMl,
    is_formula: data.isFormula,
  }),
  updateEvent: (data) => $api.events.feed.updateEventBottleFeed({
    ...data,
    name: 'feed_bottle',
    description: '',
    amount_ml: data.amountMl,
    is_formula: data.isFormula,
  }),
  onSubmit: () => {
    emit('submit');
  },
  initialState,
  isEdit: props.isEdit,
  event: props.feedEvent,
});

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

</script>

<style></style>