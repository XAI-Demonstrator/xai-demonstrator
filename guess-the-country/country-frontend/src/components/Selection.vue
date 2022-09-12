<template>
  <div class="selection">
    <section
        class="xd-section xd-light"
        v-if="showSelection">
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
    control: {
      type: Boolean,
    }
  },

  computed: {
    showSelection () {
      if (this.sequence_mode==='classic'||this.sequence_mode==='basic'){
        return (!this.user_city_answer)
      } else if (this.sequence_mode==='recommender'){
          if (this.control){return (this.prediction_city&&!this.user_city_answer)}
          else {return (this.prediction_city&&!this.user_city_answer&&this.explanation)}
      } else {
        return false
      }
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
.selection {
  width: 100%;
}

.element {
  margin-bottom: 10px;
}

.element:last-child {
  margin-bottom: 0;
}

.xd-section:last-child {
  margin-bottom: 12px;
}
</style>
