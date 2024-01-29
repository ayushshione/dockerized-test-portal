/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './portal/templates/portal/add-user.html',
    './portal/templates/portal/test-settings/*.html',
    './portal/templates/portal/admin_2.html',
    './portal/templates/portal/users-database.html',
    "./portal/templates/portal/user-login/src/**/*.{js,jsx,ts,tsx}",
    "./portal/templates/portal/user-login/src/components/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

