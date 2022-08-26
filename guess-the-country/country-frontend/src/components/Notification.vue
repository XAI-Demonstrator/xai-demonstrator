<template>
  <div>
      <section v-show="!explanation" class="xd-section xd-light" >
        <!-- Question -->
        <section v-show="showQuestion">  
          <p v-if= "sequence_mode==='classic'">Your guess: Where has this Google Streetview picture been taken?</p>
          <p v-else>Where has this Google Streetview picture been taken?</p>
        </section>   
        <!-- User guess -->
        <section v-show="showUserGuess">  
          <p class="short-text">Your guess is: {{user_city_answer}}</p>
        </section>
        <!-- control group (without explanation), AI guess -->
        <section v-show="showAIGuess&&control"> 
          <p class="short-text">My guess is: {{prediction_city}}</p>
        </section>
        <!-- treatment group (with explanation), AI guess -->
        <section v-show="showAIGuess&&!control"> 
          <p>My guess is: {{prediction_city}}
          <br>In particular, the colored areas below have helped me form my guess. </p>
          <p v-if= "sequence_mode==='recommender'">What is your guess?</p>
        </section>
      </section>
  </div>
</template>
<script>

export default {
  name: "Notification",
  props: {
      msg: {
          type: String,
          default: "Hello"
      },
       label_city: {
          type: String
      },
      user_city_answer: {
          type: String
      },
      prediction_city: {
        type: String
      },
      control:{
        type: Boolean
      },
      sequence_mode: {
        type: String
      },
  },
  computed: {
    showQuestion() {
      if (this.sequence_mode==='classic'||this.sequence_mode==='basic'){
        return !this.user_city_answer
      } else if (this.sequence_mode==='recommender'){
        return !this.prediction_city
      } else {
        return false
      }

    },
    showUserGuess() {
      if (this.sequence_mode==='classic'){
        return this.user_city_answer && !this.prediction_city
      } else if (this.sequence_mode==='recommender' || this.sequence_mode==='basic'){
        return this.user_city_answer
      } else {
        return false
      }
    },
    showAIGuess() {
      if (this.sequence_mode==='classic'){
        return this.prediction_city 
      } else if (this.sequence_mode==='recommender'){
        return this.prediction_city&&!this.user_city_answer 
      } else 
        return false
    },
  },

  data() {
    return {
    }
  }
}

</script>
<style scoped>
.xd-section:last-child{
    text-align: center;
    margin-bottom: 12px;
}
.short-text{
  line-height: 2;
}

</style>
