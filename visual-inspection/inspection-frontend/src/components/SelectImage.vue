<template>
  <div class="my-swipe" v-on:click="nextImage">
    <mt-swipe ref="images" :auto="0" v-on:change="handleChange">
      <mt-swipe-item class="my-slide slide1">
        <img class="my-image" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Cute_dog_%28427147974%29.jpg/300px-Cute_dog_%28427147974%29.jpg" />
      </mt-swipe-item>
      <mt-swipe-item class="my-slide slide2">
        <img class="my-image" src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Cute-dog-licking-lips.jpg/300px-Cute-dog-licking-lips.jpg" />
      </mt-swipe-item>
      <mt-swipe-item class="my-slide slide3"><img class="my-image" src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Cute_dog_222.jpg/300px-Cute_dog_222.jpg" />
      </mt-swipe-item>
    </mt-swipe>
  </div>
</template>

<script>
export default {
  name: "SelectImage",
  methods: {
    handleChange(index) {
      this.$emit("imageChanged", index)
    },
    nextImage() {
      this.$refs.images.next()
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

.my-slide {
  background-position: center center;
  background-repeat: no-repeat;
  overflow: hidden;
}

.my-slide img {
  min-height: 100%;
  min-width: 100%;
}

.slide1 {
  background-color: #FFCCBC;
  color: #2c3e50;
}

.slide2 {
  background-color: #D3E3FC;
  color: #000;
}

.slide3 {
  background-color:  #77A6F7;
  color: #D3E3FC;
}

</style>