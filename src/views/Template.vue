<template>
  <div class="container-flex">
    
    <TemplateSwitch v-bind:url="`${$store.state.url_prefix}/templatelist`" :add="true" />
    <FormRender msg="this is test" v-bind:editable="true" v-if="$store.getters.config.template_id" :item="$store.state.item_detail"></FormRender>
    
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";

import TemplateSwitch from "@/components/TemplateSwitch.vue"; // @ is an alias to /src
import FormRender from "@/components/FormRender.vue";

@Component({
  components: {
    TemplateSwitch,
    FormRender
  }
})
export default class Template extends Vue {}
</script>
