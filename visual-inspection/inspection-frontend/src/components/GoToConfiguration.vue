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
  name: "GoToConfiguration",

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
    "buttonText": "KI trainieren"
  },
  "en": {
    "buttonText": "Train AI"
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
