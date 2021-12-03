<!--
MIT License

The MIT License

Copyright (c) Norserium, https://github.com/Norserium

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
-->
<script>
import classnames from 'classnames';
import bem from 'easy-bem';
import {BoundingBox, DraggableArea, StencilPreview, SimpleHandler, SimpleLine} from 'vue-advanced-cropper';

const cn = bem('vue-explanation-stencil');
export default {
	name: 'ExplanationStencil',
	components: {
		StencilPreview,
		BoundingBox,
		DraggableArea,
	},
	props: {
		image: {
			type: Object,
		},
		coordinates: {
			type: Object,
		},
		stencilCoordinates: {
			type: Object,
		},
		handlers: {
			type: Object,
		},
		handlersComponent: {
			type: [Object, String],
			default() {
				return SimpleHandler;
			},
		},
		lines: {
			type: Object,
		},
		linesComponent: {
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
		resizable: {
			type: Boolean,
			default: true,
		},
		transitions: {
			type: Object,
		},
		movingClass: {
			type: String,
		},
		resizingClass: {
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
		},
    /* Modifications for XAI Demonstrator */
    explanationImg: {
      type: String,
    },
    explanationMode: {
      type: Boolean,
      default: false
    },
    /* /Modifications */
	},
	data() {
		return {
			moving: false,
			resizing: false,
      internalExplanationMode: false // Modification for XAI Demonstrator
		};
	},
  /* Modifications for XAI Demonstrator */
  watch: {
    explanationMode: function (newVal) {
      if (newVal) {
        this.internalExplanationMode = true;
      }
    }
  },
  /* /Modifications */
	computed: {
		classes() {
			return {
				stencil: classnames(
					cn({ movable: this.movable, moving: this.moving, resizing: this.resizing }),
					this.moving && this.movingClass,
					this.resizing && this.resizingClass,
				),
				preview: classnames(cn('preview'), this.previewClass),
				boundingBox: classnames(cn('bounding-box'), this.boundingBoxClass),
			};
		},
		style() {
			const { height, width, left, top } = this.stencilCoordinates;
			const style = {
				width: `${width}px`,
				height: `${height}px`,
				transform: `translate(${left}px, ${top}px)`,
			};
			if (this.transitions && this.transitions.enabled) {
				style.transition = `${this.transitions.time}ms ${this.transitions.timingFunction}`;
			}
			return style;
		},
    /* Modifications for XAI Demonstrator */
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
    /* /Modification */
	},
	methods: {
		onMove(moveEvent) {
			this.$emit('move', moveEvent);
			this.moving = true;
      this.internalExplanationMode = false; // Modification for XAI Demonstrator
		},
		onMoveEnd() {
			this.$emit('move-end');
			this.moving = false;
		},
		onResize(resizeEvent) {
			this.$emit('resize', resizeEvent);
			this.resizing = true;
      this.internalExplanationMode = false; // Modification for XAI Demonstrator
		},
		onResizeEnd() {
			this.$emit('resize-end');
			this.resizing = false;
		},
		aspectRatios() {
			return {
				minimum: this.aspectRatio || this.minAspectRatio,
				maximum: this.aspectRatio || this.maxAspectRatio,
			};
		},
	},
	emits: ['resize', 'resize-end', 'move', 'move-end'],
};
</script>

<template>
	<div :class="classes.stencil" :style="style">
		<bounding-box
			:width="stencilCoordinates.width"
			:height="stencilCoordinates.height"
			:transitions="transitions"
			:class="classes.boundingBox"
			:handlers="handlers"
			:handlers-component="handlersComponent"
			:handlers-classes="handlersClasses"
			:handlers-wrappers-classes="handlersWrappersClasses"
			:lines="lines"
			:lines-component="linesComponent"
			:lines-classes="linesClasses"
			:lines-wrappers-classes="linesWrappersClasses"
			:resizable="resizable"
			@resize="onResize"
			@resize-end="onResizeEnd"
		>
			<draggable-area :movable="movable" @move="onMove" @move-end="onMoveEnd">
				<stencil-preview
					:image="image"
					:coordinates="coordinates"
					:width="stencilCoordinates.width"
					:height="stencilCoordinates.height"
					:class="classes.preview"
					:transitions="transitions"
				/>
			</draggable-area>
      <!-- Modification for XAI Demonstrator -->
      <div v-show="internalExplanationMode" v-bind:style="explanationStyle">&nbsp;</div>
      <!-- /Modification -->
		</bounding-box>
	</div>
</template>

<style lang="scss">
.vue-rectangle-stencil {
	position: absolute;
	height: 100%;
	width: 100%;
	box-sizing: border-box;
	&__preview {
		position: absolute;
		width: 100%;
		height: 100%;
	}
	&--movable {
		cursor: move;
	}
}
</style>