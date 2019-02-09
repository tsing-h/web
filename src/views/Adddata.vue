<template>
  <div class="row">
    <div class="w-100">
      <!-- <code class="">{{ $store.getters.config }}</code> -->
    </div>
    <TemplateSwitch v-bind:url="'http://localhost:5000/clinicals/templatelist'" :add="false" class="col w-100 " />
    <FormRender msg="this is test" v-bind:edit="false" v-if="$store.getters.config.template_id"></FormRender>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import FormTemplate from "@/components/FormTemplate.vue"; // @ is an alias to /src
import TemplateSwitch from "@/components/TemplateSwitch.vue";
import Test from "@/components/Test.vue";
import FormRender from "@/components/FormRender.vue";

@Component({
  components: { FormTemplate, TemplateSwitch, Test, FormRender }
})
export default class Adddata extends Vue {}
</script>
