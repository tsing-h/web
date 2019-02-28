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
    <TemplateSwitch :url="'http://localhost:5000/clinicals/templatelist'" :add="false" v-show="$store.state.template_id == ''" />
    <FormRender :editable="false" v-if="$store.getters.config.template_id"></FormRender>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TemplateSwitch from "@/components/TemplateSwitch.vue";
import FormRender from "@/components/FormRender.vue";
import * as types from "../stores/mutations_type";

@Component({
  components: { TemplateSwitch, FormRender }
})
export default class Adddata extends Vue {
  api_url: string = "";
  created() {
    this.api_url = this.$store.state.url_prefix;
    this.$store.commit(types.ADD_ITEMS, {});
  }
  // DEBUG ONLY
  change_api_url() {
    this.$store.commit("CHANGE_API_URL", this.api_url);
  }
}
</script>
