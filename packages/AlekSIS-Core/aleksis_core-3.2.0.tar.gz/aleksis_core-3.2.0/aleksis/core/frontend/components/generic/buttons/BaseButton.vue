<template>
  <v-btn v-bind="$props" @click="$emit('click')">
    <v-icon v-if="iconText" left>{{ iconText }}</v-icon>
    <span v-t="i18nKey" />
  </v-btn>
</template>

<script>
export default {
  name: "base-button",
  inheritAttrs: true,
  extends: "v-btn",
  props: {
    i18nKey: {
      type: String,
      required: true,
    },
    iconText: {
      type: String,
      required: false,
      default: undefined,
    },
  },
};
</script>

<style scoped></style>
