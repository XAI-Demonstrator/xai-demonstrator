<template>
  <div id="highlightbox">
    <span v-for="pair in explanation" :key="pair.word + Math.random()"
          v-bind:style="{'color': 'hsl(' + ((1 + 3*pair.score) * 60) + ',100%,' + (pair.score === 0 ? 0 : 50) + '%)'}">{{
        pair.word
      }}&#32;</span>
  </div>
</template>

<script>
export default {
  name: "TextHighlight",
  props: [
    "explanation"
  ]
}
</script>

<style scoped>
#highlightbox {
  background-color: darkgray;
  padding: 10px;
}
</style>