<template>
  <div>
    <section
      class="xd-section xd-light"
      v-if="getSelectionCondition" > 
          <div v-for="city in cities" :key="city.city" class="element">
            <input
          type="Button"
          class="xd-button xd-secondary"
          v-bind:value="city.city"
          v-on:click="answer_city(city.city)"
        />
          </div>
    </section>
  </div>
</template>
<script>
export default {
  name: "Selection",
  props: {
    user_city_answer: {
      type: String,
    },
    sequence_mode: {
      type: String,
    },
    prediction_city: {
      type: String,
    },
    explanation: {
      type: Object,
    },
  },
  computed: {
    getSelectionCondition () {
      let selection_condition = this.sequence_mode==='classic'&&!this.user_city_answer
            || this.sequence_mode==='recommender'&&this.prediction_city&&!this.user_city_answer&&this.explanation
            || this.sequence_mode==='basic' && !this.user_city_answer
      return selection_condition
    }
  },
  data() {
    return {
          cities: [
            {
              city: "Tel Aviv",
              backend: "Tel_Aviv",
            },
            {
              city: "Jerusalem",
              backend: "Westjerusalem",
            },
            {
              city: "Berlin",
              backend: "Berlin",
            },
            {
              city: "Hamburg",
              backend: "Hamburg",
            }
      ],
    };
  },
  methods: {
    answer_city(city) {
      this.$emit("city_selected", city);
    },
  },
};
</script>
<style scoped>
.element {
  flex: 1;
   margin-bottom: 10px;
}
.element:last-child {
   margin-bottom: 0px;
}
.flex-style {
display: flex; 
gap: 10px
}

.xd-section:last-child {
  margin-bottom: 12px;
}



</style>
