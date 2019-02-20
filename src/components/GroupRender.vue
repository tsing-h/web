<template>
  <div class="card border w-100 mb-2"  :class="editable? 'border border-danger':''">
    <!-- 组名 -->
    <div class="card-header align-items-start"  @click="toggle_visible = !toggle_visible" v-if="!editable">
      <label class="h4 float-left mt-2">{{ group.name }}</label>
      <el-button class="el-icon-refresh float-right ml-2" @click.stop="save_group"> 保存组数据</el-button>
    </div>
    <div class="card-header align-items-start"  @click="toggle_visible = !toggle_visible" v-else>
      <div class="row" >
        <div class="input-group col-9">
          <div class="input-group-prepend">
            <span class="input-group-text">组&nbsp;&nbsp;名:</span>
          </div>
          <input type="text" v-model="group.name" class="form-control" style="height:40px" @click.stop="return false" />
        </div>
        <el-button class="col el-icon-plus  " @click.stop="show_field_dlg"> 添加列</el-button>
        <el-button class="col el-icon-delete" type="danger" @click.stop="delete_group"> 删除组X</el-button>
      </div>

      <!-- <div class="alert alert-info w-100 mt-2">
        <pre style="text-align:left">{{ JSON.stringify(group, null, 2) }}</pre>
      </div> -->
    </div>

    <el-collapse-transition>
      <ul class="list-group list-group-flush" v-show="toggle_visible" >
        <el-collapse-transition>
        <li class="list-group-item text-left" v-if="toggle_field">
          <!-- <FieldGenerate v-model="tmp_field" /> -->
          <FieldGenerate @submit="add_field"/>
        </li>
        </el-collapse-transition>
        <li class="list-group-item text-left" v-for="(field, index) in group.fields" :key="index" >
          <div class="input-group" >
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
import { CONFIG, Item } from "../store";
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
  private value!: Item;

  @Prop() private item!: Item;
  // 展开或者关闭
  toggle_visible: boolean = true;
  toggle_field: boolean = false; // 新建字段
  private value2: { [key: string]: any } = { ...this.item };

  @Watch("value2", { immediate: false, deep: true })
  onValue2Changed(val: any, oldVal: any) {
    this.$emit("input", this.value2);
  }

  @Watch("group")
  onGroupChanged(val: any, oldval: any) {
    this.value2 = {};
    console.log(this.group);
  }

  created() {
    this.value2 = { ...this.item };
  }

  // 当处于编辑模板场景时:
  tmp_field: any = {};
  // 打开编辑字段对话框
  show_field_dlg() {
    // TODO...
    // toggle_field = !toggle_field; toggle_visible = toggle_field || toggle_visible
    // 组隐藏时， 固定显示组和字段填写
    if (!this.toggle_visible) {
      this.toggle_field = true;
      this.toggle_visible = true;
    } else {
      this.toggle_field = !this.toggle_field;
    }
  }
  add_field(field_cfg) {
    console.log(field_cfg);
    // 提供template_id, group_index
    this.$store.commit(types.ADD_FIELD, {
      index_group: this.index_group,
      field: { ...field_cfg }
    });
    this.$forceUpdate();
    this.toggle_field = false;
  }

  delete_group() {
    // TODO...
    this.$store.commit(types.DELETE_GROUP, {
      index_group: this.index_group
    });
    this.$message({
      type: "warning",
      message: "模板已更新，请及时保存"
    });
    this.$emit("destroyed");
  }

  delete_field(index) {
    this.$store.commit(types.DELETE_FIELD, {
      index_group: this.index_group,
      index_field: index
    });
    this.$forceUpdate();
    this.$message({
      type: "info",
      message: "模板已更新，请及时保存"
    });
  }

  save_group() {
    // TODO 需要出发后端交互
    // this.$store.dispatch(types.ACTION_SAVE_GROUP, {
    //   group: this.group.name,
    //   value: this.value2
    // });
    // this.$message({
    //   type: "success",
    //   message: "模板已更新成功"
    // });
    this.$emit("submit");
  }
}
</script>
