<template>
  <div class="home">
    <h4>Detail</h4>
    <!-- <code class="card">{{ $store.state.item_detail }}</code> -->
    <div class="input-group col-sm-4 pl-0 float-left mt-1" v-for="(item, index) in current_item" :key="index">
      <div class="input-group-prepend">
        <span class="input-group-text">{{ index }}</span>
      </div>
      <input type="text" class="form-control" :placeholder="item">
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

@Component({
  components: {}
})
export default class Detail extends Vue {
  public get current_item(): any {
    return this.$store.state.item_detail;
  }
}
</script>
