<template>
  <UModal :open="open" :title="title" :description="description" :dismissible="dismissible" :overlay="overlay"
    :transition="transition" :fullscreen="fullscreen" :portal="portal" :close="close" :close-icon="closeIcon" :ui="ui"
    @update:open="onUpdateOpen">
    <!-- BODY -->
    <template #body>
      <div class="px-4 py-3">
        <slot />
      </div>
    </template>

    <!-- OPTIONAL header passthrough (advanced usage) -->
    <template #header="{ close }">
      <slot name="header" :close="close" />
    </template>

    <!-- FOOTER -->
    <template #footer>
      <slot name="footer" :confirm="() => emit('confirm')" :cancel="() => emit('cancel')">
        <div class="flex gap-2 justify-end">
          <UButton :label="cancelText" :color="cancelColor" :variant="cancelVariant" :size="size" type="button"
            @click="emit('cancel')" />
          <UButton :label="confirmText" :color="confirmColor" :variant="confirmVariant" :size="size" :icon="confirmIcon"
            :loading="confirmLoading" :disabled="confirmDisabled" type="button" @click="emit('confirm')" />
        </div>
      </slot>
    </template>
  </UModal>
</template>

<script setup lang="ts">
/**
 * ConfirmDialog.vue
 *
 * A controlled confirmation dialog built on top of Nuxt UI's UModal.
 * - Emits: `confirm`, `cancel`
 * - Parent controls visibility via the `open` prop.
 *
 * Best-practices:
 *  - Strongly typed props & emits
 *  - Do NOT self-close the modal; instead, emit and let the parent decide
 *  - Map overlay/escape dismissal to `cancel` (accessible + predictable)
 *  - Forward key UModal props and offer button customization props
 *
 * Docs:
 *  - UModal props, slots, update:open emit: https://ui.nuxt.com/components/modal
 *  - UButton props (color, variant, loading, type): https://ui.nuxt.com/components/button
 */

defineOptions({ name: 'ConfirmDialog' })

type ButtonColor =
  | 'primary'
  | 'secondary'
  | 'success'
  | 'info'
  | 'warning'
  | 'error'
  | 'neutral'

type ButtonVariant = 'solid' | 'outline' | 'soft' | 'subtle' | 'ghost' | 'link'
type ButtonSize = 'sm' | 'md' | 'lg' | 'xl'

interface Props {
  /** Controls visibility (parent-owned state) */
  open: boolean

  /** Header content */
  title?: string
  description?: string

  /** Body copy is provided via default slot */

  /** Whether clicking overlay / pressing ESC should try to dismiss */
  dismissible?: boolean

  /** Common UModal options forwarded */
  overlay?: boolean
  transition?: boolean
  fullscreen?: boolean
  portal?: boolean | string
  close?: boolean | Record<string, unknown> // allow passing Button props or `false`
  closeIcon?: string
  /** Pass-through to customize Modal UI classes (Nuxt UI `ui` prop) */
  ui?: Record<string, unknown>

  /** Footer button customization */
  confirmText?: string
  cancelText?: string
  confirmColor?: ButtonColor
  cancelColor?: ButtonColor
  confirmVariant?: ButtonVariant
  cancelVariant?: ButtonVariant
  size?: ButtonSize
  confirmIcon?: string
  cancelIcon?: string
  confirmLoading?: boolean
  confirmDisabled?: boolean
}

withDefaults(defineProps<Props>(), {
  open: false,
  // Modal
  dismissible: true,
  overlay: true,
  transition: true,
  fullscreen: false,
  portal: true,
  close: true,
  closeIcon: undefined,
  ui: () => ({ footer: 'justify-end' }),
  // Buttons
  confirmText: 'Confirm',
  cancelText: 'Cancel',
  confirmColor: 'primary',
  cancelColor: 'neutral',
  confirmVariant: 'solid',
  cancelVariant: 'outline',
  size: 'md',
  confirmIcon: undefined,
  cancelIcon: undefined,
  confirmLoading: false,
  confirmDisabled: false
})

const emit = defineEmits<{
  /** User explicitly confirmed */
  confirm: []
  /** User cancelled OR dismissed (overlay/ESC/close button) */
  cancel: []
}>()

/**
 * If the internal modal tries to change `open` (e.g., overlay click or ESC),
 * we translate that to `cancel` and let the parent decide to close.
 */
function onUpdateOpen(next: boolean) {
  if (!next) emit('cancel')
}
</script>
