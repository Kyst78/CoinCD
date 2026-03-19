<script setup lang="ts">
import { reactive } from "vue";
import { handleError } from "~/utils/error";
import AuthButton from "~/components/Auth/AuthButton.vue";
import type { FormSubmitEvent } from "#ui/types";
import { loginSchema, registerSchema } from "~/utils/schemas";
import type { LoginSchema, RegisterSchema } from "~/utils/schemas";
import useStore from "~/composables/useStore";

const loginForm = reactive({ email: "", password: "" });
const registerForm = reactive({ email: "", password: "", name: "" });

const { isLoading, toggleLoading, showMessage, showError } = useStore();
const { fetch: refreshSession } = useUserSession();
const activeTab = ref<'login' | 'register'>('login');

async function login(event: FormSubmitEvent<LoginSchema>) {
  try {
    toggleLoading(true);
    await $fetch("/api/auth/login", { method: "POST", body: event.data });
    showMessage({ title: "เข้าสู่ระบบสำเร็จ", description: "กำลังนำคุณไปยังหน้าหลัก..." });
    await new Promise((resolve) => setTimeout(resolve, 1000));
    await refreshSession();
    await navigateTo("/coin", { replace: true });
  } catch (error) {
    showError(handleError(error));
  } finally {
    toggleLoading(false);
  }
}

async function register(event: FormSubmitEvent<RegisterSchema>) {
  try {
    toggleLoading(true);
    await $fetch("/api/auth/register", { method: "POST", body: event.data });
    showMessage({ title: "สมัครสมาชิกสำเร็จ", description: "บัญชีของคุณถูกสร้างเรียบร้อยแล้ว" });
    await new Promise((resolve) => setTimeout(resolve, 1000));
    await refreshSession();
    await navigateTo("/coin", { replace: true });
  } catch (error: any) {
    showError(handleError(error));
  } finally {
    toggleLoading(false);
  }
}

definePageMeta({ layout: "auth" });
</script>

<template>
  <div class="w-full max-w-md">

    <!-- Brand -->
    <div class="flex items-center justify-center gap-3 mb-7">
      <div class="relative">
        <div class="w-9 h-9 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center shadow-lg">
          <Icon name="lucide:calculator" class="w-4 h-4 text-white" />
        </div>
        <div class="absolute -top-0.5 -right-0.5 w-3 h-3 bg-green-400 rounded-full border-2 border-white" />
      </div>
      <span class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        CoinLens
      </span>
    </div>

    <!-- Card -->
    <div class="bg-white rounded-2xl shadow-xl border border-indigo-50 overflow-hidden">

      <!-- Tabs -->
      <div class="grid grid-cols-2 gap-1.5 p-2 bg-slate-50/80 border-b border-slate-100">
        <button
          @click="activeTab = 'login'"
          :class="[
            'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200',
            activeTab === 'login'
              ? 'bg-gradient-to-r from-white-500 to-purple-500 text-blue-600 shadow-md scale-[1.02]'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/70'
          ]"
        >
          เข้าสู่ระบบ
        </button>
        <button
          @click="activeTab = 'register'"
          :class="[
            'py-2.5 px-4 rounded-xl text-sm font-semibold transition-all duration-200',
            activeTab === 'register'
              ? 'bg-gradient-to-r from-white-500 to-purple-500 text-blue-600 shadow-md scale-[1.02]'
              : 'text-slate-500 hover:text-slate-700 hover:bg-white/70'
          ]"
        >
          สมัครสมาชิก
        </button>
      </div>

      <div class="px-7 py-7">

        <!-- Login -->
        <div v-if="activeTab === 'login'">

          <UForm :schema="loginSchema" class="space-y-4" @submit="login" :state="loginForm">
            <UFormGroup label="อีเมล" name="email">
              <UInput v-model="loginForm.email" type="email" placeholder="กรอกอีเมลของคุณ" size="lg" :disabled="isLoading" />
            </UFormGroup>
            <UFormGroup label="รหัสผ่าน" name="password">
              <UInput v-model="loginForm.password" type="password" placeholder="กรอกรหัสผ่าน" size="lg" :disabled="isLoading" />
            </UFormGroup>

            <div class="space-y-3 pt-2">
              <UButton block size="lg" type="submit" :loading="isLoading" :disabled="isLoading"
                class="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-semibold rounded-xl shadow-lg shadow-blue-200 hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200">
                {{ isLoading ? "กำลังเข้าสู่ระบบ..." : "เข้าสู่ระบบ" }}
              </UButton>

              <div class="relative flex items-center gap-3">
                <div class="flex-1 h-px bg-slate-200" />
                <span class="text-xs text-slate-400 font-medium">หรือ</span>
                <div class="flex-1 h-px bg-slate-200" />
              </div>

              <AuthButton :disabled="isLoading" class="w-full" />
            </div>
          </UForm>
        </div>

        <!-- Register -->
        <div v-if="activeTab === 'register'">

          <UForm :schema="registerSchema" class="space-y-4" @submit="register" :state="registerForm">
            <UFormGroup label="ชื่อ" name="name">
              <UInput v-model="registerForm.name" placeholder="กรอกชื่อของคุณ" size="lg" :disabled="isLoading" />
            </UFormGroup>
            <UFormGroup label="อีเมล" name="email">
              <UInput v-model="registerForm.email" type="email" placeholder="กรอกอีเมลของคุณ" size="lg" :disabled="isLoading" />
            </UFormGroup>
            <UFormGroup label="รหัสผ่าน" name="password">
              <UInput v-model="registerForm.password" type="password" placeholder="กรอกรหัสผ่าน" size="lg" :disabled="isLoading" />
            </UFormGroup>

            <div class="space-y-3 pt-2">
              <UButton block size="lg" type="submit" :loading="isLoading" :disabled="isLoading"
                class="bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-semibold rounded-xl shadow-lg shadow-blue-200 hover:shadow-xl hover:-translate-y-0.5 transition-all duration-200">
                {{ isLoading ? "กำลังสมัครสมาชิก..." : "สมัครสมาชิก" }}
              </UButton>

              <div class="relative flex items-center gap-3">
                <div class="flex-1 h-px bg-slate-200" />
                <span class="text-xs text-slate-400 font-medium">หรือ</span>
                <div class="flex-1 h-px bg-slate-200" />
              </div>

              <AuthButton :disabled="isLoading" class="w-full" />
            </div>
          </UForm>
        </div>

      </div>
    </div>

    <p class="text-center mt-4 text-xs text-slate-400">
      กดดำเนินการต่อถือว่ายอมรับ
      <a href="#" class="text-indigo-400 hover:underline">เงื่อนไข</a> &amp;
      <a href="#" class="text-indigo-400 hover:underline">นโยบายความเป็นส่วนตัว</a>
    </p>

  </div>
</template>