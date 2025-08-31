import { reactive, ref } from 'vue';
import type { FormSubmitEvent } from '@nuxt/ui';
import type * as v from 'valibot';

// Define the expected shape of form data with date and time fields
interface FormData {
  date: string;
  time: string;
  [key: string]: unknown;
}

// Constrain the schema to ensure it includes date and time fields
type EventFormSchema = v.ObjectSchema<
  v.ObjectEntries & {
    date: v.BaseSchema<unknown, string, v.BaseIssue<unknown>>;
    time: v.BaseSchema<unknown, string, v.BaseIssue<unknown>>;
    notes: v.BaseSchema<unknown, string | null | undefined, v.BaseIssue<unknown>>;
  },
  undefined
>;

interface UseEventFormParams<T extends EventFormSchema, U> {
  schema: T;
  createEvent: (data: v.InferOutput<T> & {
    id: string;
    time_start: string;
    time_end: string;
  }) => Promise<U>;
  updateEvent: (data: v.InferOutput<T> & {
    id: string;
    time_start: string;
    time_end: string;
  }) => Promise<U>;
  onSubmit: (formEvent: FormSubmitEvent<v.InferOutput<T>>) => void | Promise<void>;
  initialState: v.InferOutput<T>;
  isEdit: boolean;
  event?: { id?: string; time_start: string; notes?: string | null };
}

export function useEventForm<T extends EventFormSchema, U>(
  params: UseEventFormParams<T, U>
) {
  const { createEvent, updateEvent, initialState, isEdit, event } = params;

  const toast = useToast();
  const isLoading = ref(false);
  const eventStore = useEventStore();

  // Create state with proper typing
  const state = reactive(initialState) as v.InferOutput<T> & FormData;

  if (isEdit && event) {
    state.date = new Date(event.time_start).toLocaleDateString('en-CA');
    state.time = dateToLocalTimeString(new Date(event.time_start));
  } else {
    state.date = new Date().toLocaleDateString('en-CA');
    state.time = dateToLocalTimeString(new Date());
  }

  async function onSubmit(formEvent: FormSubmitEvent<v.InferOutput<T>>) {
    isLoading.value = true;
    try {
      // Type guard to ensure formEvent.data has the required properties
      const formData = formEvent.data as v.InferOutput<T> & FormData;

      const [hours, minutes] = formData.time.split(':').map(Number);
      if (hours === undefined) {
        throw new Error('Hours is unexpectedly undefined.', { cause: formData.time });
      }


      function parseLocalDate(dateString: string): Date {
        const [year, month, day] = dateString.split('-').map(Number);
        if (!year || !month || !day) throw new Error('Invalid date string');
        return new Date(year, month - 1, day);
      }

      const combinedDate = parseLocalDate(formData.date);
      combinedDate.setHours(hours, minutes, 0, 0);
      const timeStart: string = combinedDate.toISOString();

      const eventPayload = {
        ...formData,
        id: event?.id ?? '',
        time_start: timeStart,
        time_end: timeStart, // Assuming time_end is the same as time_start for now...TODO: this is invalid for pumping + breast feeding.
      };

      if (isEdit) {
        await updateEvent(eventPayload);
      } else {
        await createEvent(eventPayload);
      }

      eventStore.clearEditState();
      toast.add({
        title: `Event ${isEdit ? 'updated' : 'created'} successfully`,
        color: 'success',
      });

      params.onSubmit(formEvent);

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An unknown error occurred';
      console.error(`Error ${isEdit ? 'updating' : 'creating'} event`, error);
      toast.add({
        title: `Error ${isEdit ? 'updating' : 'creating'} event`,
        description: errorMessage,
        color: 'error',
      });
    } finally {
      isLoading.value = false;
    }
  }

  return {
    state,
    onSubmit,
    isLoading,
  };
}