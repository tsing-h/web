<template>
  <div class="row">
    <div class="w-100">
      <!-- <code class="">{{ $store.getters.config }}</code> -->
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

    <TemplateSwitch v-bind:url="'http://localhost:5000/clinicals/templatelist'" :add="false" class="col w-100 " />
    <FormRender msg="this is test" v-bind:edit="false" v-if="$store.getters.config.template_id" :item="$store.state.item_detail"></FormRender>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TemplateSwitch from "@/components/TemplateSwitch.vue";
import FormRender from "@/components/FormRender.vue";
import { Item, State } from "../store";

@Component({
  components: { TemplateSwitch, FormRender }
})
export default class Showdata extends Vue {
  api_url: string = "";
  item: Item = {};
  created() {
    this.api_url = this.$store.state.url_prefix;
    this.item = this.$store.state.item_detail;
  }
  // DEBUG ONLY
  change_api_url() {
    this.$store.commit("CHANGE_API_URL", this.api_url);
  }
}
</script>
