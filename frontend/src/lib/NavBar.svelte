<script lang="ts">
  let mobileMenuOpen = false
  let profileOpen = false
  let username= "User"
</script>

<nav class="fixed inset-x-0 top-0 z-10 h-16 bg-gray-900 border-b-2 border-b-sky-400/90 shadow-[0_0_102px_4px] shadow-sky-400/90">
  <div class="mx-auto px-2 sm:px-6 lg:px-8">
    <div class="relative flex h-16 items-center justify-between">
      <!-- Mobile -->
      <div class="absolute inset-y-0 left-0 flex items-center sm:hidden">
        <button type="button" class="inline-flex items-center rounded-md p-2 text-white hover:text-sky-400 cursor-pointer transition duration-200" on:click={() => (mobileMenuOpen = !mobileMenuOpen)} aria-controls="mobile-menu" aria-expanded={mobileMenuOpen}>
          <span class="sr-only">Toggle menu</span>
          <span class="icon-[iconamoon--menu-burger-horizontal-bold] text-2xl leading-none"></span>
        </button>
      </div>

      <!-- Nav links -->
      <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
        <div class="flex shrink-0 items-center">
          <img class="h-9 w-9" src="/logo.png" alt="Logo" />
        </div>
        <div class="hidden sm:ml-6 sm:block">
          <div class="flex space-x-4">
            <a href="/" class="text-white hover:text-sky-400 px-3 py-2 text-m font-medium transition duration-200">Home</a>
            <a href="/sshPayloads" class="text-white hover:text-sky-400 px-3 py-2 text-m font-medium transition duration-200">SSH</a>
            <a href="/apiPayloads" class="text-white hover:text-sky-400 px-3 py-2 text-m font-medium transition duration-200">API</a>
            <a href="/users" class="text-white hover:text-sky-400 px-3 py-2 text-m font-medium transition duration-200">Users</a>
            <a href="/about" class="text-white hover:text-sky-400 px-3 py-2 text-m font-medium transition duration-200">Transtion Test</a>
          </div>
        </div>
      </div>

      <!-- Profile -->
      <div class="absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0">
        <div class="ml-3 relative">
          <div class="flex items-center">
            <span class="text-white mr-2 cursor-default">{username}</span>
            <button type="button" class="lex items-center cursor-pointer rounded-full text-sm border-3 border-transparent hover:border-3 hover:border-sky-400 transition duration-200" id="user-menu-button" on:click={() => (profileOpen = !profileOpen)} aria-expanded={profileOpen} aria-haspopup="true">
              <span class="sr-only">Open user menu</span>
              <img class="h-9 w-9 rounded-full" src="/user.png" alt="User"/>
            </button>
          </div>

          {#if profileOpen}
            <div class="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-gray-800 py-1" role="menu" aria-labelledby="user-menu-button">
              <a href="/profile" class="block px-4 py-2 text-sm text-white hover:text-sky-400 transition duration-200" role="menuitem">Your Profile</a>
              <a href="/settings" class="block px-4 py-2 text-sm text-white hover:text-sky-400 transition duration-200" role="menuitem">Settings</a>
              <a href="/signout" class="block px-4 py-2 text-sm text-white hover:text-sky-400 transition duration-200" role="menuitem">Sign out</a>
            </div>
          {/if}
        </div>
      </div>
    </div>
  </div>

  {#if mobileMenuOpen}
    <div class="sm:hidden" id="mobile-menu">
      <div class="space-y-1 px-2 pt-2 pb-3">
        <a href="/" class="text-white block  hover:bg-gray-700 hover:text-sky-400 rounded-md px-3 py-2 text-base font-medium transition duration-200">Home</a>
        <a href="/sshPayloads" class="text-white hover:bg-gray-700 hover:text-sky-400 block rounded-md px-3 py-2 text-base font-medium transition duration-200">SSH</a>
        <a href="/apiPayloads" class="text-white hover:bg-gray-700 hover:text-sky-400 block rounded-md px-3 py-2 text-base font-medium transition duration-200">API</a>
        <a href="/users" class="text-white hover:bg-gray-700 hover:text-sky-400 block rounded-md px-3 py-2 text-base font-medium transition duration-200">Users</a>
      </div>
    </div>
  {/if}
</nav>

