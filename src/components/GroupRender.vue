<template>
  <div class="card border w-100 mb-2"  >
    <!-- 组名 -->
    <div class="card-header align-items-start"  @click="toggle_visible = !toggle_visible">
      <label class="h4 float-left mt-2">{{ group.name }}</label>
      <el-button class="el-icon-refresh float-right ml-2" @click="save_group"> 保存</el-button>
    </div>
    <el-collapse-transition>
      <ul class="list-group list-group-flush" v-show="toggle_visible">
        <!-- <li class="list-group-item text-left" v-if="cur_group == index_group">
          <el-collapse-transition>
            <FieldGenerate v-model="tmp_field" @submit="addfield" />
          </el-collapse-transition>
        </li> -->
        <li class="list-group-item text-left border-top-0" v-for="(field, index) in group.fields" :key="index">
          <div class="input-group">
            <FieldRender v-bind:field="field" class="col" v-if="field.label" v-model="value2[field.name]"/>
            <el-button class="el-icon-delete " @click="delete_field(index)" v-if="editable"> 移除</el-button>
          </div>
        </li>
      </ul>
    </el-collapse-transition> 
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import axios from "axios";
import FieldGenerate from "@/components/FieldGenerate.vue";
import FieldRender from "@/components/FieldRender.vue";
// Vue.component("FieldGenerate", FieldGenerate);
// Vue.component("FieldRender", FieldRender);
import { CONFIG } from "../store";
import * as types from "../stores/mutations_type";

interface GROUP {
  name: string;
  type: string;
  [key: string]: any;
}
@Component({
  components: { FieldGenerate, FieldRender }
})
export default class GroupRender extends Vue {
  @Prop({ default: false, type: Boolean })
  private editable!: boolean;
  @Prop() private group!: GROUP;
  @Prop({ type: Number, default: 0 })
  private index_group!: number;
  @Prop({
    default: () => {
      return {};
    }
  })
  private value!: any;

  // 展开或者关闭
  toggle_visible: boolean = true;
  private value2: { [key: string]: any } = { ...this.value };

  @Watch("value2", { immediate: false, deep: true })
  onValue2Changed(val: any, oldVal: any) {
    this.$emit("input", this.value2);
  }

  @Watch("group")
  onGroupChanged(val: any, oldval: any) {
    this.value2 = {};
    console.log(this.group);
  }

  delete_field(index) {
    this.$store.commit(types.DELETE_FIELD, {
      group_index: this.index_group,
      field_index: index
    });
    this.$forceUpdate();
  }

  save_group() {
    // TODO
    this.$store.dispatch(types.ACTION_SAVE_GROUP, {
      group: this.group.name,
      value: this.value2
    });
  }

  // mounted() {
  //   console.log("mounted", this.group);
  // }
  // beforeUpdate() {
  //   console.log("beforeUpdate");
  // }
  // updated() {
  //   console.log("updated");
  // }
}
</script>
