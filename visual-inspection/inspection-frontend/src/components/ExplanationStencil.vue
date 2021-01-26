<!--
MIT License

Copyright (c) 2019-2020 Norserium

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
-->
<script>
import classnames from 'classnames';
import bem from 'easy-bem';
import {BoundingBox, DraggableArea, PreviewResult, SimpleHandler, SimpleLine} from 'vue-advanced-cropper';

const cn = bem('vue-explanation-stencil');
export default {
  name: 'ExplanationStencil',
  components: {
    PreviewResult,
    BoundingBox,
    DraggableArea,
  },
  props: {
    img: {
      type: Object,
    },
    explanationImg: {
      type: String,
    },
    explanationMode: {
      type: Boolean,
      default: false
    },
    resultCoordinates: {
      type: Object,
    },
    stencilCoordinates: {
      type: Object,
    },
    handlers: {
      type: Object,
    },
    handlerComponent: {
      type: [Object, String],
      default() {
        return SimpleHandler;
      },
    },
    lines: {
      type: Object,
    },
    lineComponent: {
      type: [Object, String],
      default() {
        return SimpleLine;
      },
    },
    aspectRatio: {
      type: [Number, String],
    },
    minAspectRatio: {
      type: [Number, String],
    },
    maxAspectRatio: {
      type: [Number, String],
    },
    movable: {
      type: Boolean,
      default: true,
    },
    scalable: {
      type: Boolean,
      default: true,
    },
    transitions: {
      type: Object,
    },
    draggingClass: {
      type: String,
    },
    previewClass: {
      type: String,
    },
    boundingBoxClass: {
      type: String,
    },
    linesClasses: {
      type: Object,
      default() {
        return {};
      },
    },
    linesWrappersClasses: {
      type: Object,
      default() {
        return {};
      },
    },
    handlersClasses: {
      type: Object,
      default() {
        return {};
      },
    },
    handlersWrappersClasses: {
      type: Object,
      default() {
        return {};
      },
    }
  },
  data() {
    return {
      dragging: false,
      internalExplanationMode: false,
    };
  },
  watch: {
    explanationMode: function (newVal) {
      if (newVal) {
        this.internalExplanationMode = true;
      }
    }
  },
  computed: {
    classes() {
      return {
        stencil: classnames(
            cn({movable: this.movable, dragging: this.dragging}),
            this.classname,
            this.dragging && this.draggingClass,
        ),
        preview: classnames(cn('preview'), this.previewClass || this.previewClassname),
        boundingBox: classnames(cn('bounding-box'), this.boundingBoxClass || this.boundingBoxClassname),
      };
    },
    style() {
      const {height, width, left, top} = this.stencilCoordinates;
      const style = {
        width: `${width}px`,
        height: `${height}px`,
        left: `${left}px`,
        top: `${top}px`,
      };
      if (this.transitions && this.transitions.enabled) {
        style.transition = `${this.transitions.time}ms ${this.transitions.timingFunction}`;
      }
      return style;
    },
    explanationStyle() {
      return {
        position: 'absolute',
        width: '100%',
        height: '100%',
        'background-repeat': 'no-repeat',
        'background-image': 'url(' + this.explanationImg + ')',
        'z-index': 0,
        'background-size': 'cover'
      }
    }
  },
  methods: {
    onMove(moveEvent) {
      this.$emit('move', moveEvent);
      this.dragging = true;
      this.internalExplanationMode = false;
    },
    onMoveEnd() {
      this.$emit('move-end');
      this.dragging = false;
    },
    onResize(resizeEvent) {
      this.$emit('resize', resizeEvent);
      this.dragging = true;
      this.internalExplanationMode = false;
    },
    onResizeEnd() {
      this.$emit('resize-end');
      this.dragging = false;
    },
    aspectRatios() {
      return {
        minimum: this.aspectRatio || this.minAspectRatio,
        maximum: this.aspectRatio || this.maxAspectRatio,
      };
    },
  },
};
</script>

<template>
  <div :class="classes.stencil" :style="style">
    <BoundingBox
        :class="classes.boundingBox"
        :handlers="handlers"
        :handler-component="handlerComponent"
        :handlers-classes="handlersClasses"
        :handlers-wrappers-classes="handlersWrappersClasses"
        :lines="lines"
        :line-component="lineComponent"
        :lines-classes="linesClasses"
        :lines-wrappers-classes="linesWrappersClasses"
        :scalable="scalable"
        @resize="onResize"
        @resize-end="onResizeEnd"
    >
      <DraggableArea ref="draggable" :movable="movable" @move="onMove" @move-end="onMoveEnd">
        <PreviewResult
            :img="img"
            :class="classes.preview"
            :transitions="transitions"
            :stencil-coordinates="stencilCoordinates"
        />
        <div v-show="internalExplanationMode" v-bind:style="explanationStyle">&nbsp;
        </div>
      </DraggableArea>

    </BoundingBox>
  </div>
</template>

<style lang="scss">
.vue-explanation-stencil {
  position: absolute;
  height: 100%;
  width: 100%;
  box-sizing: border-box;

  &--movable {
    cursor: move;
  }
}
</style>