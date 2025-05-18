<script>
import NavBar from "$lib/NavBar.svelte";
</script>

<header>
    <NavBar />
</header>
<main class="p-16 pt-28 overflow-auto tall:overflow-hidden">
    <slot />
</main>