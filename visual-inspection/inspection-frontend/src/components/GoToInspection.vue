<template>
  <div>
    <div class="explanation-request">
      <button class="xd-button xd-secondary">
          {{ $t('buttonText') }}
      </button>

    </div>
  </div>
</template>

<script>
export default {
  name: "GoToInspection",

  data() {
    return {
      waitingForExplanation: false
    }
  }
}
</script>

<i18n>
{
  "de": {
    "buttonText": "KI trainieren und zurückkehren"
  },
  "en": {
    "buttonText": "Train AI and return"
  }
}
</i18n>

<style scoped>
.explanation-request {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 60px;
}

</style>
