<script>
import BaseButton from "./BaseButton.vue";
export default {
  name: "secondary-action-button",
  components: { BaseButton },
  extends: BaseButton,
  props: {
    i18nKey: {
      type: String,
      required: true,
    },
    color: {
      type: String,
      required: false,
      default: "secondary",
    },
    outlined: {
      type: Boolean,
      required: false,
      default: true,
    },
  },
};
</script>
