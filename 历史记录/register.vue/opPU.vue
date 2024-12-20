<template>
    <div class="register-container">
      <div class="register-box">
        <h2 class="register-title">创建新账户</h2>
        <el-form :model="form" :rules="rules" ref="form" label-position="top">
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
              @input="checkPasswordStrength"
            ></el-input>
            <div class="password-strength">
              <div class="strength-bar" :style="{ width: passwordStrength + '%' }"></div>
            </div>
            <span class="strength-text">{{ passwordStrengthText }}</span>
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
              prefix-icon="el-icon-message"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="手机号码" prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号码"
              prefix-icon="el-icon-mobile-phone"
              clearable
            ></el-input>
          </el-form-item>
  
          <el-form-item label="验证码" prop="captcha">
            <el-row :gutter="10">
              <el-col :span="16">
                <el-input
                  v-model="form.captcha"
                  placeholder="请输入验证码"
                ></el-input>
              </el-col>
              <el-col :span="8">
                <el-button type="primary" @click="sendCaptcha" :disabled="captchaDisabled">
                  {{ captchaText }}
                </el-button>
              </el-col>
            </el-row>
          </el-form-item>
  
          <el-form-item>
            <el-checkbox v-model="form.agree">
              我已阅读并同意
              <el-link type="primary" @click="showAgreement">《用户协议》</el-link>
              和
              <el-link type="primary" @click="showPrivacy">《隐私政策》</el-link>
            </el-checkbox>
          </el-form-item>
  
          <el-form-item>
            <el-button type="primary" @click="submitForm" :loading="loading">注册</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, reactive } from 'vue'
  import { ElMessage } from 'element-plus'
  
  export default {
    name: 'GrayRegistrationPage',
    setup() {
      const form = reactive({
        username: '',
        password: '',
        confirmPassword: '',
        email: '',
        phone: '',
        captcha: '',
        agree: false
      })
  
      const rules = {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 6, max: 20, message: '用户名长度在6-20个字符之间', trigger: 'blur' },
          { pattern: /^[a-zA-Z]/, message: '用户名必须以字母开头', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 6, message: '密码至少6个字符', trigger: 'blur' },
          { pattern: /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/, message: '密码必须包含字母和数字', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请确认密码', trigger: 'blur' },
          { validator: (rule, value, callback) => {
            if (value !== form.password) {
              callback(new Error('两次输入的密码不一致'))
            } else {
              callback()
            }
          }, trigger: 'blur' }
        ],
        email: [
          { required: true, message: '请输入邮箱', trigger: 'blur' },
          { type: 'email', message: '邮箱格式不正确', trigger: ['blur', 'change'] }
        ],
        phone: [
          { required: true, message: '请输入手机号码', trigger: 'blur' },
          { pattern: /^[1][3-9][0-9]{9}$/, message: '手机号码格式不正确', trigger: 'blur' }
        ],
        captcha: [
          { required: true, message: '请输入验证码', trigger: 'blur' }
        ],
        agree: [
          { validator: (rule, value, callback) => {
            if (!value) {
              callback(new Error('请阅读并同意用户协议和隐私政策'))
            } else {
              callback()
            }
          }, trigger: 'change' }
        ]
      }
  
      const formRef = ref(null)
      const loading = ref(false)
      const captchaDisabled = ref(false)
      const captchaText = ref('发送验证码')
      const passwordStrength = ref(0)
      const passwordStrengthText = ref('')
  
      const checkPasswordStrength = () => {
        const password = form.password
        let strength = 0
        if (password.length >= 6) strength += 20
        if (password.match(/[A-Z]/)) strength += 20
        if (password.match(/[a-z]/)) strength += 20
        if (password.match(/[0-9]/)) strength += 20
        if (password.match(/[^A-Za-z0-9]/)) strength += 20
        passwordStrength.value = strength
  
        if (strength < 40) passwordStrengthText.value = '弱'
        else if (strength < 80) passwordStrengthText.value = '中'
        else passwordStrengthText.value = '强'
      }
  
      const sendCaptcha = () => {
        if (!form.phone) {
          ElMessage.warning('请先输入手机号码')
          return
        }
        captchaDisabled.value = true
        let count = 60
        const timer = setInterval(() => {
          if (count > 0) {
            captchaText.value = `${count}秒后重试`
            count--
          } else {
            clearInterval(timer)
            captchaDisabled.value = false
            captchaText.value = '发送验证码'
          }
        }, 1000)
        // 这里添加发送验证码的逻辑
        ElMessage.success('验证码已发送')
      }
  
      const submitForm = () => {
        if (!formRef.value) return
        formRef.value.validate((valid) => {
          if (valid) {
            loading.value = true
            // 这里添加注册逻辑
            setTimeout(() => {
              loading.value = false
              ElMessage.success('注册成功')
              // 注册成功后的操作，如跳转到登录页
            }, 2000)
          } else {
            ElMessage.error('请正确填写所有必填项')
            return false
          }
        })
      }
  
      const showAgreement = () => {
        ElMessage('这里显示用户协议内容')
      }
  
      const showPrivacy = () => {
        ElMessage('这里显示隐私政策内容')
      }
  
      return {
        form,
        rules,
        formRef,
        loading,
        captchaDisabled,
        captchaText,
        passwordStrength,
        passwordStrengthText,
        checkPasswordStrength,
        sendCaptcha,
        submitForm,
        showAgreement,
        showPrivacy
      }
    }
  }
  </script>
  
  <style scoped>
  .register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 20px;
  }
  
  .register-box {
    width: 100%;
    max-width: 450px;
    padding: 40px;
    background-color: #ffffff;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border-radius: 20px;
    transition: all 0.3s ease;
  }
  
  .register-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  }
  
  .register-title {
    text-align: center;
    margin-bottom: 30px;
    font-size: 28px;
    color: #333;
    font-weight: 600;
  }
  
  .el-form-item {
    margin-bottom: 25px;
  }
  
  .el-input__inner {
    border-radius: 8px;
    border: 1px solid #d4d4d4;
    transition: all 0.3s ease;
  }
  
  .el-input__inner:focus {
    border-color: #909399;
    box-shadow: 0 0 0 2px rgba(144, 147, 153, 0.2);
  }
  
  .el-button {
    width: 100%;
    border-radius: 8px;
    font-size: 16px;
    height: 44px;
    transition: all 0.3s ease;
  }
  
  .el-button--primary {
    background-color: #606266;
    border-color: #606266;
  }
  
  .el-button--primary:hover, .el-button--primary:focus {
    background-color: #909399;
    border-color: #909399;
  }
  
  .el-checkbox {
    margin-top: 10px;
    color: #606266;
  }
  
  .password-strength {
    height: 4px;
    background-color: #e0e0e0;
    margin-top: 5px;
    border-radius: 2px;
    overflow: hidden;
  }
  
  .strength-bar {
    height: 100%;
    transition: width 0.3s ease;
    background-color: #909399;
  }
  
  .strength-text {
    font-size: 12px;
    color: #606266;
    margin-top: 5px;
    display: inline-block;
  }
  
  .el-link {
    font-weight: 400;
    color: #606266;
  }
  
  .el-link:hover {
    color: #909399;
  }
  
  @media (max-width: 480px) {
    .register-box {
      padding: 30px 20px;
    }
  }
  </style>