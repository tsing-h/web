<template>
  <div class="form-inline row">
    <label class="mr-1 d-block text-right" style="width:90px">{{ field.label }}:</label>
    <!-- number(int, float) -->
    <input 
      type="number" 
      class="form-control" 
      :placeholder="'Enter '+field.label" 
      v-model="value2" 
      v-if="field.type=='number'" 
      style="width:1%; flex:1 auto"
      @input="handle_model()"
    >
    
    <!-- select -->
    <div class="card border-0" v-if="field.type=='select'" style="flex: auto">
      <!-- selcet -->
      <el-select 
        v-model="value2" 
        :name="field.name" 
        :placeholder="'请选择'+field.label" 
        :multiple="field.multiple" 
        v-if="field.type=='select'" 
        style="width:100%; flex:1 auto"
        @input="handle_model()"
        @change="sub_values={}"
      >
        <el-option
          v-for="item in field.values"
          :key="item.value"
          :label="item.value"
          :value="item.value">
        </el-option>
      </el-select>

      <!-- subs 单选框，选择某个特定项后出现额外填写内容-->
      <div class="w-100 mt-1" v-if="field.type=='select' && !field.multiple ">
        <!-- 遍历field.values -->
        <div class="w-100 " v-for="(field_value, field_index) in sub_items(value2)" :key="field_index">
          <!-- 判断并遍历value.subs -->
          <div class="input-group mt-1"
            v-for="(sub_item, sub_index) in field_value.subs" :key="sub_index"
          >
            <div class="input-group-prepend">
              <span class="input-group-text">{{ sub_item.label }}</span>
            </div>
            <input type="text" :placeholder="'Enter '+sub_item.label" class="form-control" v-model="sub_values[sub_item.name]"  @blur="handle_select()">
          </div>
        </div>
        
      </div>
    </div>

    <!-- file -->
    <el-upload
      v-if="field.type=='file'"
      :name="field.name"
      :action="'http://localhost:5000/clinicals/upload/imgs'"
      :multiple="field.multiple"
      :auto-upload="true"
      list-type="picture-card"
      show-file-list
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-preview="handlePictureCardPreview"
    >
      <i class="el-icon-plus"></i>
    </el-upload>
    <el-dialog :visible.sync="dialogVisible" v-if="field.type=='file'">
      <img width="100%" :src="dialogImageUrl" alt="">
    </el-dialog>

    <!-- text -->
    <el-input 
      :placeholder="'Enter '+field.label" 
      v-model="value2" 
      v-if="field.type=='text'" 
      style="width:1%; flex:1 auto"
      @input="handle_model()"
    ></el-input>
    <!-- textarea -->
    <el-input 
      type="textarea" :rows="2" 
      :placeholder="'Enter '+field.label" 
      v-model="value2" 
      v-if="field.type=='textarea'" 
      style="width:1%; flex:1 auto"
      @input="handle_model()"
    ></el-input>

    <!-- datetime -->
    <el-date-picker
      v-model="value2" v-if="field.type=='datetime'" style="width:1%; flex:1 auto"
      type="datetime"
      :name="field.name"
      placeholder="选择日期时间"
      @input="handle_model()"
    >
    </el-date-picker>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Emit, Vue } from "vue-property-decorator";

interface FieldOption {
  name: string;
  label: string;
}
interface FieldType {
  [key: string]: any;
}

@Component
export default class FieldRender extends Vue {
  @Prop() private field!: FieldType;

  @Prop({ default: "" })
  private value!: any;

  @Prop({ type: Boolean, default: false })
  private editable!: boolean;

  public get sub_items(): Function {
    return (value: string) => {
      return this.field.values.filter(field_value => {
        return field_value.subs && value == field_value.value;
      });
    };
  }

  value2: any = this.value;

  @Watch("field")
  onFieldChanged(val: any, oldval: any) {
    this.value2 = this.value;
  }

  handle_model() {
    this.$emit("input", this.value2);
  }

  handle_select() {
    this.$emit("input", { value: this.value2, subs: this.sub_values });
    this.$forceUpdate();
  }
  // value: any = "";
  // 选择型字段附加的子字段
  sub_values: any = {};
  // 文件型字段
  upload_url: string = "";

  // 表单支持的类型

  field_types: FieldOption[] = [
    { name: "number", label: "数字" },
    { name: "text", label: "字符串" },
    { name: "textarea", label: "段落" },
    { name: "file", label: "文件" },
    { name: "datetime", label: "日期时间" },
    { name: "select", label: "选择" }
  ];

  dialogImageUrl: string = "";
  dialogVisible: boolean = false;

  handleSuccess(err: any, file: any, fileList: any) {
    console.log(err, file, fileList);
  }
  handleRemove(err: any, file: any, fileList: any) {
    // 从服务器上删除该文件
    console.log(err, file, fileList);
  }
  handleError(
    err: any,
    file: { name: string; url: string },
    fileList: Array<{ name: string; url: string }>
  ) {
    console.log(err, file, fileList);
  }
  handlePictureCardPreview(file: any) {
    console.log(file);
  }
}
</script>
