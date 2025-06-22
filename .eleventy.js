module.exports = function (eleventyConfig) {
  // Copia le cartelle di asset nella cartella finale.
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/admin");

  // Ritorna la configurazione delle directory.
  // Questa è la configurazione standard di settore.
  return {
    passthroughFileCopy: true,
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes", // La cartella è RELATIVA all'input
      layouts: "_layouts"    // Specifichiamo anche la cartella dei layout
    },
  };
};