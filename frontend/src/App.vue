<script setup>

import { ref } from 'vue'
import axios from 'axios'

const api = 'http://localhost:32469'

const loggedIn = ref(false)

const loginUsername = ref('')
const loginPassword = ref('')

const registerUsername = ref('')
const registerPassword = ref('')

const students = ref([])

const form = ref({
  name: '',
  email: '',
  age: '',
  english_level: 'Principiante'
})

const editingId = ref(null)

const notification = ref('')
const notificationType = ref('success')

const showNotification = (message, type = 'success') => {

  notification.value = message

  notificationType.value = type

  setTimeout(() => {

    notification.value = ''

  }, 3000)
}

const login = async () => {

  try {

    await axios.post(`${api}/login`, {
      username: loginUsername.value,
      password: loginPassword.value
    })

    loggedIn.value = true
    showNotification('Login exitoso')

    loginUsername.value = ''
    loginPassword.value = ''

    getStudents()

  } catch (error) {

    showNotification(
  error.response.data.message,
  'error'
)
  }
}

const register = async () => {

  try {

    const response = await axios.post(
      `${api}/register`,
      {
        username: registerUsername.value,
        password: registerPassword.value
      }
    )

    showNotification(response.data.message)

    registerUsername.value = ''
registerPassword.value = ''

  } catch (error) {

    showNotification(
  error.response.data.message,
  'error'
)
  }
}

const logout = () => {

  loggedIn.value = false
}

const getStudents = async () => {

  const response = await axios.get(
    `${api}/students`
  )

  students.value = response.data
}

const saveStudent = async () => {

  if (editingId.value) {

    await axios.put(
      `${api}/students/${editingId.value}`,
      form.value
    )

  } else {

    await axios.post(
      `${api}/students`,
      form.value
    )
  }

  resetForm()

  getStudents()
}

const editStudent = (student) => {

  editingId.value = student.id

  form.value = {
    name: student.name,
    email: student.email,
    age: student.age,
    english_level: student.english_level
  }
}

const deleteStudent = async (id) => {

  await axios.delete(
    `${api}/students/${id}`
  )

  getStudents()
}

const resetForm = () => {

  editingId.value = null

  form.value = {
    name: '',
    email: '',
    age: '',
    english_level: 'Principiante'
  }
}

</script>

<template>


  <!-- NOTIFICATION -->

<div
  v-if="notification"
  class="
    fixed
    top-5
    right-5
    z-50
    px-6
    py-4
    rounded-xl
    shadow-2xl
    text-white
    font-semibold
    transition-all
  "

  :class="

    notificationType === 'success'

    ? 'bg-green-500'

    : 'bg-red-500'

  "
>

  {{ notification }}

</div>

<!-- LOGIN -->

<div
  v-if="!loggedIn"
  class="min-h-screen flex"
>

  <!-- LEFT -->

  <div
    class="
      w-1/2
      flex
      items-center
      justify-center
      bg-white
      p-16
    "
  >

    <div class="w-full max-w-md">

      <h1
        class="
          text-5xl
          font-bold
          mb-10
        "
      >
        Sign In
      </h1>

      <!-- LOGIN -->

      <input
        v-model="loginUsername"
        placeholder="Username"
        class="
          w-full
          border
          p-4
          rounded-xl
          mb-5
        "
      />

      <input
        type="password"
        v-model="loginPassword"
        placeholder="Password"
        class="
          w-full
          border
          p-4
          rounded-xl
          mb-5
        "
      />

      <button
        @click="login"
        class="
          w-full
          bg-pink-500
          hover:bg-pink-600
          text-white
          p-4
          rounded-xl
          transition
        "
      >
        Login
      </button>

      <!-- REGISTER -->

      <div class="mt-10">

        <h2 class="text-2xl font-bold mb-5">

          Create Account

        </h2>

        <input
          v-model="registerUsername"
          placeholder="New Username"
          class="
            w-full
            border
            p-4
            rounded-xl
            mb-5
          "
        />

        <input
          type="password"
          v-model="registerPassword"
          placeholder="New Password"
          class="
            w-full
            border
            p-4
            rounded-xl
            mb-5
          "
        />

        <button
          @click="register"
          class="
            w-full
            bg-black
            hover:bg-gray-800
            text-white
            p-4
            rounded-xl
            transition
          "
        >
          Register
        </button>

      </div>

    </div>

  </div>

  <!-- RIGHT -->

  <div
    class="
      w-1/2
      bg-gradient-to-br
      from-fuchsia-500
      via-purple-600
      to-blue-500
      flex
      items-center
      justify-center
    "
  >

    <div
      class="
        text-white
        text-center
        p-10
      "
    >

      <h1 class="text-6xl font-bold mb-5">
        Student System
      </h1>

      <p class="text-xl opacity-90">
        Kubernetes + Docker + Vue + Flask + MongoDB
      </p>

    </div>

  </div>

</div>

<!-- DASHBOARD -->

<div
  v-else
  class="
    min-h-screen
    bg-gray-100
    p-10
  "
>

  <!-- NAVBAR -->

  <div
    class="
      flex
      justify-between
      items-center
      mb-10
    "
  >

    <h1
      class="
        text-4xl
        font-bold
      "
    >
      Student Dashboard
    </h1>

    <button
      @click="logout"
      class="
        bg-red-500
        hover:bg-red-600
        text-white
        px-6
        py-3
        rounded-xl
      "
    >
      Logout
    </button>

  </div>

  <div class="grid grid-cols-3 gap-10">

    <!-- FORM -->

    <div
      class="
        bg-white
        p-8
        rounded-2xl
        shadow-lg
      "
    >

      <h2
        class="
          text-2xl
          font-bold
          mb-6
        "
      >

        {{ editingId ? 'Edit Student' : 'New Student' }}

      </h2>

      <input
        v-model="form.name"
        placeholder="Name"
        class="
          w-full
          border
          p-4
          rounded-xl
          mb-5
        "
      />

      <input
        v-model="form.email"
        placeholder="Email"
        class="
          w-full
          border
          p-4
          rounded-xl
          mb-5
        "
      />

      <input
        v-model="form.age"
        placeholder="Age"
        class="
          w-full
          border
          p-4
          rounded-xl
          mb-5
        "
      />

      <select
        v-model="form.english_level"
        class="
          w-full
          border
          p-4
          rounded-xl
          mb-5
        "
      >

        <option>
          Principiante
        </option>

        <option>
          Intermedio
        </option>

        <option>
          Avanzado
        </option>

      </select>

      <button
        @click="saveStudent"
        class="
          w-full
          bg-blue-600
          hover:bg-blue-700
          text-white
          p-4
          rounded-xl
        "
      >

        {{ editingId ? 'Update Student' : 'Create Student' }}

      </button>

    </div>

    <!-- TABLE -->

    <div
      class="
        col-span-2
        bg-white
        p-8
        rounded-2xl
        shadow-lg
      "
    >

      <h2
        class="
          text-2xl
          font-bold
          mb-6
        "
      >
        Students
      </h2>

      <table class="w-full">

        <thead>

          <tr class="border-b">

            <th class="text-left p-4">
              Name
            </th>

            <th class="text-left p-4">
              Email
            </th>

            <th class="text-left p-4">
              Age
            </th>

            <th class="text-left p-4">
              English
            </th>

            <th class="text-left p-4">
              Actions
            </th>

          </tr>

        </thead>

        <tbody>

          <tr
            v-for="student in students"
            :key="student.id"
            class="border-b"
          >

            <td class="p-4">
              {{ student.name }}
            </td>

            <td class="p-4">
              {{ student.email }}
            </td>

            <td class="p-4">
              {{ student.age }}
            </td>

            <td class="p-4">
              {{ student.english_level }}
            </td>

            <td class="p-4 flex gap-3">

              <button
                @click="editStudent(student)"
                class="
                  bg-yellow-400
                  px-4
                  py-2
                  rounded-lg
                "
              >
                Edit
              </button>

              <button
                @click="deleteStudent(student.id)"
                class="
                  bg-red-500
                  text-white
                  px-4
                  py-2
                  rounded-lg
                "
              >
                Delete
              </button>

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>

</div>

</template>