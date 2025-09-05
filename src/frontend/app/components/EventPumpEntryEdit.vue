<template>
  <UForm
:schema="pumpEventSchema" :state="state" class="flex flex-col justify-between gap-10 h-full"
    @submit="onSubmit">
    <div class="h-full flex flex-col gap-5">
      <!-- Amount -->
      <div class="flex flex-col  gap-3">
        <div class="flex flex-row justify-between w-full">
          <label class="font-bold">Amount</label>
          <span class="opacity-80 flex flex-row ">
            <input v-model="state.amountMl" type="number" :min="0" :max="200" class="[appearance:textfield] text-right decoration-dashed underline"  >
            <span>
            ml ({{ mlToOz(state.amountMl, 1) }}oz)
          </span>
          </span>
        </div>




        <UFormField name="amountMl">
          <USlider
v-model="state.amountMl" size="xl" :min="0" :max="200" :ui="{
            track: 'h-9 rounded-sm',
            range: 'rounded-sm rounded-r-none ',
            thumb: 'h-9 w-2 rounded-sm'
          }" />
        </UFormField>
      </div>

          <!-- Duration -->
      <div class="flex flex-col  gap-3">
        <div class="flex flex-row justify-between w-full">
          <label class="font-bold">Duration</label>
          <span class="opacity-80">{{ state.duration }} minutes</span>
        </div>

        <UFormField name="duration">
          <USlider v-model="state.duration" size="xl" :min="0" :max="60" :ui="{
            track: 'h-9 rounded-sm',
            range: 'rounded-sm rounded-r-none ',
            thumb: 'h-9 w-2 rounded-sm'
          }" />
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
    </div>
    <UButton size="xl" block type="submit" :loading="isLoading">
      {{ isEdit ? 'Edit Pump' : 'Log Pump' }}
    </UButton>
  </UForm>
</template>

<script lang="ts" setup>
import * as v from 'valibot'
import { useEventForm } from '~/composables/useEventForm';
import type { IAPIPumpEvent } from '~~/repository/modules/pump/types';

const emit = defineEmits<{
  submit: [],
  cancel: []
}>()

const props = withDefaults(defineProps<{
  event?: IAPIPumpEvent
  isEdit?: boolean
}>(), {
  event: undefined
})

const { $api } = useNuxtApp()
const eventStore = useEventStore();

const pumpEventSchema = v.object({
  amountMl: v.pipe(v.number()),
  duration: v.pipe(v.number()),
  time: v.pipe(v.string()),
  date: v.pipe(v.string()),
  notes: v.nullish(v.pipe(v.string()))
})

type PumpEventSchema = v.InferOutput<typeof pumpEventSchema>

const startingPumpData = props.event ? props.event : await eventStore.getDefaultPumpEventData();

// The server only stores start/end times, not duration. So, we need
// to manually calculate the duration if there is an event passed
// in to us so that we can show it in the "edit" version of the component.
const pumpDurationMinutes = startingPumpData.time_end ? (new Date(startingPumpData.time_end).getTime() - new Date(startingPumpData.time_start).getTime()) / 60000 : 30;


const initialState: PumpEventSchema = {
  amountMl: startingPumpData.amount_ml,
  duration: pumpDurationMinutes,
  date: '', // Will be set by the composable
  time: '', // Will be set by the composable
  notes: props.isEdit ? startingPumpData.notes : undefined
};

const { state, onSubmit, isLoading } = useEventForm<typeof pumpEventSchema, IAPIPumpEvent>({
  schema: pumpEventSchema,
  createEvent: (data) => $api.events.pump.createEventPump({
    ...data,
    name: 'pump',
    description: '',
    // Here we need to convert from a duration to a time_end.
    time_end: state.duration ? new Date(new Date(data.time_start).getTime() + (state.duration * 60000)).toISOString() : undefined,
    amount_ml: data.amountMl,
  }),
  updateEvent: (data) => $api.events.pump.updateEventPump({
    ...data,
    name: 'pump',
    description: '',
    // Here we need to convert from a duration to a time_end.
    time_end: state.duration ? new Date(new Date(data.time_start).getTime() + (state.duration * 60000)).toISOString() : undefined,
    amount_ml: data.amountMl,
  }),
  onSubmit: () => {
    emit('submit');
  },
  initialState,
  isEdit: props.isEdit,
  event: props.event,
});


</script>

<style></style>