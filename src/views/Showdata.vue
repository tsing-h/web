<template>
  <div class="row">
    <div class="w-100">
      <!-- <code class="">{{  $route.params.id }} <br>{{ $store.state.item_detail }}</code> -->
    </div>
    <div class="input-group mb-1" v-show="false">
      <div class="input-group-prepend">
        <span class="input-group-text">测试URL</span>
      </div>
      <input type="text" class="form-control" v-model="api_url">
      <div class="input-group-append">
        <span class="input-group-text">/adddata</span>
      </div>
      <div class="input-group-append">
        <button class="btn btn-outline-secondary" @click="change_api_url">Change</button>
      </div>
    </div>

    <TemplateSwitch v-bind:url="`${$store.state.url_prefix}/templatelist`" :add="false" @change_template="handleTemplateChange" />
    <FormRender v-bind:editable="false" v-if="$store.getters.config.template_id" :item="item" ref="FormRender"></FormRender>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TemplateSwitch from "@/components/TemplateSwitch.vue";
import FormRender from "@/components/FormRender.vue";
import * as types from "../stores/mutations_type";
import { Item, State } from "../store";

@Component({
  components: { TemplateSwitch, FormRender }
})
export default class Showdata extends Vue {
  api_url: string = "";
  item: Item = {};
  item_id: number = 1;
  created() {
    this.api_url = this.$store.state.url_prefix;
    this.item = this.$store.state.item_detail || null;
    if (!this.item.id) {
      this.$store
        .dispatch(types.ACTION_FETCH_ITEM, this.$route.params.id)
        .then(rst => {
          this.item = this.$store.state.item_detail || null;
          this.$forceUpdate();
        });
    }
  }
  // DEBUG ONLY
  change_api_url() {
    this.$store.commit("CHANGE_API_URL", this.api_url);
  }

  handleTemplateChange() {
    (this.$refs["FormRender"] as any).$forceUpdate();
  }
}
</script>
