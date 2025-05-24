<script lang="ts">
	import '../app.css';
    import { onNavigate } from "$app/navigation";

    onNavigate(() => {
        if (!document.startViewTransition) {
            return;
        }

        return new Promise<void>((resolve) => {
            document.startViewTransition(() => {
                resolve();
            })
        })
    })
</script>

<main class="overflow-auto tall:overflow-hidden">
    <slot />
</main>
