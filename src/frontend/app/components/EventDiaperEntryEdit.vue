<template>
    <UForm :schema="diaperSchema" :state="state" class="flex flex-col justify-between gap-10 h-full" @submit="onSubmit">
        <div class="h-full flex flex-col gap-5">
            <!-- Type -->
            <UFormField name="diaperType">

                <div class="flex flex-col gap-3">


                    <label class="font-bold">Diaper Type</label>

                    <URadioGroup size="xl" variant="card" v-model="state.diaper_type" :items="diaperTypeItems"
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



            <!-- Size -->
            <UFormField name="size">
                <div class="flex flex-col gap-3">
                    <label class="font-bold">Size</label>

                    <URadioGroup size="xl" variant="card" v-model="state.diaper_contents_size" :items="diaperSizeItems"
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

            <!-- Time + Date -->
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

            <!-- Show the color, consistency, and notes under "more" -->
            <UAccordion :items="[{ label: 'Color, Consistency, and Notes', icon: 'i-mdi-plus' }]">
                <template #body>
                    <div class="flex flex-col sm:flex-row flex-wrap sm:items-center gap-5 mt-3">
                        <!-- Color -->
                        <UFormField name="color">
                            <div class="flex flex-col gap-3">
                                <label class="font-bold">Color</label>

                                <!-- A radio button-based selector for the diaper color, colored for easily
                                    selection by tired parents. -->
                                <URadioGroup v-model="state.diaper_contents_color" :items="diaperColorItems"
                                    orientation="horizontal" variant="card" indicator="hidden" :ui="{
                                        fieldset: 'flex flex-col sm:flex-row flex-wrap gap-2 sm:items-center justify-between md:justify-start w-full',
                                        item: 'flex-grow'
                                    }">
                                    <template #label="{ item }">
                                        <div class="flex flex-row items-center gap-3">
                                            <!-- Color Indicator Rounded Square -->
                                            <span :class="`block w-4 h-4 rounded-md bg-${item.color}`"></span>
                                            <div :class="`flex flex-row items-center gap-1`">
                                                <span>{{ item.label }}</span>
                                            </div>
                                        </div>
                                    </template>
                                </URadioGroup>
                            </div>
                        </UFormField>

                        <!-- Consistency, Enum-based with icons for ease of selection-->
                        <UFormField name="consistency">
                            <div class="flex flex-col gap-3">
                                <label class="font-bold">Consistency</label>
                                <URadioGroup v-model="state.diaper_contents_consistency" :items="diaperConsistencyItems"
                                    orientation="horizontal" variant="card" indicator="hidden" :ui="{
                                        fieldset: 'flex flex-row flex-wrap items-center justify-between md:justify-start w-full',
                                        item: 'flex-grow'
                                    }">
                                    <template #label="{ item }">
                                        <div class="flex flex-row items-center gap-3">
                                            <UIcon :name="item.icon" class="text-2xl" />
                                            <div :class="`flex flex-row items-center gap-1`">
                                                <span>{{ item.label }}</span>
                                            </div>
                                        </div>
                                    </template>
                                </URadioGroup>
                            </div>
                        </UFormField>

                        <!-- Notes -->
                        <UFormField name="notes">
                            <div class="flex flex-col gap-3">
                                <label class="font-bold">Notes</label>
                                <UTextarea v-model="state.notes" placeholder="Add any additional notes here..." />
                            </div>
                        </UFormField>
                    </div>
                </template>
            </UAccordion>
        </div>
        <UButton size="xl" block type="submit">
            {{ isEdit ? 'Edit Diaper' : 'Log Diaper' }}
        </UButton>
    </UForm>
</template>

<script lang="ts" setup>
import type { IAPIDiaperChangeEvent, IAPIDiaperColor, IAPIDiaperConsistency } from '~~/repository/modules/diaper/types';
import { DiaperColor, DiaperConsistency, DiaperSize, DiaperType, toDiaperColor, toDiaperConsistency, toDiaperSize, toDiaperType } from "~~/types/diaper"
import * as v from 'valibot'
import type { FormSubmitEvent, RadioGroupItem } from '@nuxt/ui';
const emit = defineEmits<{
    submit: [],
    cancel: []
}>()

const props = withDefaults(defineProps<{
    event?: IAPIDiaperChangeEvent
    isEdit?: boolean
}>(), {
    event: undefined
})

const toast = useToast()

const isLoading = ref(false)

const eventStore = useEventStore()

const { $api } = useNuxtApp()

const startingDiaperData: IAPIDiaperChangeEvent = props.event ? props.event : await eventStore.getDefaultDiaperEventData();

const diaperSchema = v.object({
    time: v.pipe(v.string()),
    date: v.pipe(v.string()),
    diaper_type: v.pipe(v.enum(DiaperType)),
    diaper_contents_color: v.pipe(v.nullish(v.fallback(v.enum(DiaperColor), DiaperColor.BROWN))),
    diaper_contents_consistency: v.pipe(v.nullish(v.fallback(v.enum(DiaperConsistency), DiaperConsistency.PASTY))),
    diaper_contents_size: v.pipe(v.nullish(v.fallback(v.enum(DiaperSize), DiaperSize.MEDIUM))),
    notes: v.pipe(v.nullish(v.string()))
})

type DiaperChangeSchema = v.InferOutput<typeof diaperSchema>



const state: DiaperChangeSchema = reactive({
    // Extract only the date part from the ISO string
    // to set as the default value for the date input
    // If no date is provided, use today's date
    // in YYYY-MM-DD format
    date: (props.event && props.isEdit) ? new Date(props.event.time_start).toLocaleDateString('en-CA') : new Date().toLocaleDateString('en-CA'),
    time: (props.event && props.isEdit) ? dateToLocalTimeString(new Date(props.event.time_start)) : dateToLocalTimeString(new Date()),
    diaper_type: toDiaperType(startingDiaperData.diaper_type),
    diaper_contents_color: toDiaperColor(startingDiaperData.diaper_contents_color),
    diaper_contents_consistency: toDiaperConsistency(startingDiaperData.diaper_contents_consistency),
    diaper_contents_size: toDiaperSize(startingDiaperData.diaper_contents_size),
    notes: startingDiaperData.notes
})

const diaperTypeItems = ref<RadioGroupItem[]>([
    {
        label: "Both",
        icon: "i-mdi-emoticon-cool",
        value: DiaperType.BOTH
    },
    {
        label: "Pee",
        icon: "i-mdi-water",
        value: DiaperType.PEE,
    },
    {
        label: "Poop",
        icon: "i-mdi-emoticon-poop",
        value: DiaperType.POOP
    },
])

const diaperSizeItems = ref<RadioGroupItem[]>([
    {
        label: "Small",
        icon: "i-mdi-water-outline",
        value: DiaperSize.SMALL
    },
    {
        label: "Medium",
        icon: "i-mdi-water",
        value: DiaperSize.MEDIUM
    },
    {
        label: "Large",
        icon: "i-mdi-water-plus",
        value: DiaperSize.LARGE
    },
])

const diaperColorItems: Ref<{ label: string, value: IAPIDiaperColor, color: string }[]> = ref([
    { label: 'Brown', value: 'brown', color: 'amber-800' },
    { label: 'Yellow', value: 'yellow', color: 'yellow-500' },
    { label: 'Green', value: 'green', color: 'green-500' },
    { label: 'Black', value: 'black', color: 'gray-800' },
])

const diaperConsistencyItems: Ref<{ label: string, value: IAPIDiaperConsistency, icon: string }[]> = ref([
    { label: 'Pasty', value: 'pasty', icon: 'i-mdi-emoticon-poop' },
    { label: 'Watery', value: 'watery', icon: 'i-mdi-liquid-spot' },
])

async function onSubmit(event: FormSubmitEvent<DiaperChangeSchema>) {

    isLoading.value = true

    try {
        // Split the "HH:MM" string
        const [hours, minutes] = event.data.time.split(":").map(Number);

        if (hours === undefined) throw new Error("Hours is unexpectedly undefined.", { cause: event.data.time })

        /**
         * Handle the JS Date constructor quirks - if you pass it a date
         * it will assume it's UTC and convert to local time, which is not what we want.
         * @param dateString Date string in YYYY-MM-DD format
         */
        function parseLocalDate(dateString: string): Date {
            const [year, month, day] = dateString.split("-").map(Number);
            // Check for invalid date parts
            if (!year || !month || !day) throw new Error("Invalid date string");
            return new Date(year, month - 1, day); // local midnight
        }

        // Clone the date to avoid mutating original
        const combinedDate = parseLocalDate(event.data.date);

        // Set the hours/minutes on that date
        combinedDate.setHours(hours, minutes, 0, 0);


        // Format as ISO string for the API
        const timeStart: string = combinedDate.toISOString();

        console.log(props.event?.id, "foo")

        const newDiaperChange: IAPIDiaperChangeEvent = {
            name: "diaper_change",
            description: "",
            id: props.event ? props.event.id : "",
            time_start: timeStart,
            diaper_type: event.data.diaper_type,
            diaper_contents_color: event.data.diaper_contents_color,
            diaper_contents_consistency: event.data.diaper_contents_consistency,
            diaper_contents_size: event.data.diaper_contents_size,
            time_end: timeStart,
            notes: event.data.notes
        }

        if (props.isEdit) {
            await $api.events.diaper.updateEventDiaper(newDiaperChange)
        } else {
            await $api.events.diaper.createEventDiaper(newDiaperChange)
        }

        eventStore.clearEditState()

        toast.add({
            title: "Diaper Change Logged",
            color: "success",
        })

        emit('submit')

    } catch (e) {

        console.error("Error creating new diaper change event", e)

    } finally {
        isLoading.value = false
    }

}
</script>

<style></style>