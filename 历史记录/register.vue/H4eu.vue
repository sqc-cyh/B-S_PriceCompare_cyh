<template>
    <div class="register-container">
      <div class="register-box">
        <h2 class="register-title">创建新账户</h2>
        <el-form :model="form" :rules="rules" ref="form" label-width="120px">
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="6-20个字符，字母开头"
              prefix-icon="el-icon-user"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="密码" prop="password">
            <el-input
              v-model="form.password"
              type="password"
              placeholder="至少6个字符，包含字母和数字"
              prefix-icon="el-icon-lock"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="form.confirmPassword"
              type="password"
              placeholder="请确认密码"
              prefix-icon="el-icon-lock"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="form.email"
              placeholder="请输入邮箱"
              prefix-icon="el-icon-mail"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="手机号码" prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号码"
              prefix-icon="el-icon-phone"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="验证码" prop="captcha">
            <el-row>
              <el-col :span="16">
                <el-input
                  v-model="form.captcha"
                  placeholder="请输入验证码"
                ></el-input>
              </el-col>
              <el-col :span="8">
                <el-button type="primary" @click="sendCaptcha">发送验证码</el-button>
              </el-col>
            </el-row>
          </el-form-item>
  
          <el-form-item>
            <el-checkbox v-model="form.agree">我已阅读并同意《用户协议》和《隐私政策》</el-checkbox>
          </el-form-item>
  
          <el-form-item>
            <el-button type="primary" @click="submitForm">注册</el-button>
            <el-button type="default" @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'RegisterPage',
    data() {
      return {
        form: {
          username: '',
          password: '',
          confirmPassword: '',
          email: '',
          phone: '',
          captcha: '',
          agree: false
        },
        rules: {
          username: [
            { required: true, message: '请输入用户名', trigger: 'blur' },
            { min: 6, max: 20, message: '用户名长度在6-20个字符之间', trigger: 'blur' },
            { pattern: /^[a-zA-Z]/, message: '用户名必须以字母开头', trigger: 'blur' }
          ],
          password: [
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 6, message: '密码至少6个字符', trigger: 'blur' }
          ],
          confirmPassword: [
            { required: true, message: '请确认密码', trigger: 'blur' },
            { validator: this.validateConfirmPassword, trigger: 'blur' }
          ],
          email: [
            { required: true, message: '请输入邮箱', trigger: 'blur' },
            { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'change'] }
          ],
          phone: [
            { required: true, message: '请输入手机号码', trigger: 'blur' },
            { pattern: /^[0-9]{11}$/, message: '手机号码格式不正确', trigger: 'blur' }
          ],
          captcha: [
            { required: true, message: '请输入验证码', trigger: 'blur' }
          ],
          agree: [
            { required: true, message: '请阅读用户协议', trigger: 'change' }
          ]
        }
      }
    },
    methods: {
      validateConfirmPassword(rule, value, callback) {
        if (value !== this.form.password) {
          callback(new Error('两次输入的密码不一致'));
        } else {
          callback();
        }
      },
      sendCaptcha() {
        console.log('发送验证码到手机:', this.form.phone);
        // 这里可以添加发送验证码的逻辑
      },
      submitForm() {
        this.$refs.form.validate((valid) => {
          if (valid) {
            console.log('注册成功', this.form);
            // 这里可以添加 API 调用代码
          } else {
            console.log('表单验证失败');
            return false;
          }
        });
      },
      resetForm() {
        this.$refs.form.resetFields();
      }
    }
  }
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background: linear-gradient(to right, #ece9e6, #ffffff);
  }
  
  .register-box {
    width: 400px;
    padding: 30px;
    background-color: #fff;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    transition: all 0.3s ease;
  }
  
  .register-title {
    text-align: center;
    margin-bottom: 25px;
    font-size: 28px;
    color: #333;
  }
  
  .el-input__inner {
    border-radius: 5px;
    border: 1px solid #dcdfe6;
  }
  
  .el-button {
    width: 100%;
    border-radius: 5px;
  }
  
  .el-checkbox {
    margin-top: 10px;
  }
  </style>