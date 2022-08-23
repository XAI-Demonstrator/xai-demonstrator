<template>
  <div>
      <section v-show="!explanation" class="xd-section xd-light" >
        <!-- Question -->
        <section v-show="getQuestionCondition">  
          <p v-show= "sequence_mode==='classic'">Your guess: Where has this Google Streetview picture been taken?</p>
          <p v-show= "sequence_mode==='basic'||sequence_mode==='recommender'">Where has this Google Streetview picture been taken?</p>
        </section>   
        <!-- User guess -->
        <section v-show="getUserGuessCondition">  
          <p class="short-text">Your guess is: {{user_city_answer}}</p>
        </section>
        <!-- control group (without explanation), AI guess -->
        <section v-show="getAIGuessCondition_control"> 
          <p class="short-text">My guess is: {{prediction_city}}</p>
        </section>
        <!-- treatment group (with explanation), AI guess -->
        <section v-show="getAIGuessCondition_treatment"> 
          <p>My guess is: {{prediction_city}}
          <br>In particular, the colored areas below have helped me form my guess. </p>
          <p v-show= "sequence_mode==='recommender'">What is your guess?</p>
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
    getQuestionCondition() {
      let question_condition = this.sequence_mode==='classic'&&!this.user_city_answer
                  || this.sequence_mode==='recommender'&&!this.prediction_city
                  || this.sequence_mode==='basic'&&!this.user_city_answer
      return question_condition
    },
    getUserGuessCondition() {
      let user_guess_condition = this.sequence_mode==='classic'&&this.user_city_answer && !this.prediction_city
                  || this.sequence_mode==='recommender'&&this.user_city_answer
                  || this.sequence_mode==='basic' && this.user_city_answer
      return user_guess_condition
    },
    getAIGuessCondition_control() {
      let ai_guess_condition_control = this.sequence_mode==='classic'&&this.prediction_city && this.control
                  || this.sequence_mode==='recommender'&& this.prediction_city&&!this.user_city_answer && this.control
      return ai_guess_condition_control
    },
    getAIGuessCondition_treatment() {
      let ai_guess_condition_treatment = this.sequence_mode ==='classic' && this.prediction_city && !this.control
                  || this.sequence_mode==='recommender' &&this.prediction_city&&!this.user_city_answer && !this.control
      return ai_guess_condition_treatment
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
