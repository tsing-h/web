<template>
  <div class="about">
    <h1>This is an about page</h1>
    <TemplateSwitch v-bind:url="template_url" :add="false" class="col " />
    <code> {{ $store.state.temlate_list }} </code>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TemplateSwitch from "@/components/TemplateSwitch.vue";
Vue.component("TemplateSwitch", TemplateSwitch);

@Component
export default class About extends Vue {
  template_url: string = "http://localhost:5000/clinicals/templatelist";
}
// export default Vue.extend({
// })
</script>
