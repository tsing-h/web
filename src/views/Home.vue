<template>
  <div class="home">
    <ClinicalTemplate msg="ClinicalTemplate"/>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import ClinicalTemplate from "@/components/ClinicalTemplate.vue"; // @ is an alias to /src

@Component({
  components: {
    ClinicalTemplate
  }
})
export default class Home extends Vue {}
</script>
