module.exports = {
    content: [
        './src/**/*.{html,js,svelte,ts}',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        function ({ addVariant }) {
            addVariant('tall', '@media (min-height: 850px)');
        },
    ],
};