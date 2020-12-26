<template>
  <div class="my-swipe">
    <mt-swipe :auto="0" v-on:change="handleChange">
      <mt-swipe-item class="slide1">1</mt-swipe-item>
      <mt-swipe-item class="slide2">2</mt-swipe-item>
      <mt-swipe-item class="slide3">3</mt-swipe-item>
    </mt-swipe>
  </div>
</template>

<script>
export default {
  name: "SelectImage",
  methods: {
    handleChange(index) {
      this.$emit("imageChanged", index)
    }
  }
}
</script>

<style scoped>
.my-swipe {
  height: 100%;
  color: #fff;
  font-size: 30px;
  text-align: center;
}

.slide1 {
  background-color: #0089dc;
  color: #fff;
}

.slide2 {
  background-color: #ffd705;
  color: #000;
}

.slide3 {
  background-color: #ff2d4b;
  color: #fff;
}
</style>