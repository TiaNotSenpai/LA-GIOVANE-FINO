module.exports = function (eleventyConfig) {
  // Copia le cartelle di asset (CSS, JS, Immagini) nella cartella finale.
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/images");
  
  // Aggiungi la cartella del CMS quando la useremo.
  eleventyConfig.addPassthroughCopy("src/admin");

  // Ritorna la configurazione delle directory.
  // Questa è la configurazione standard che NON può fallire.
  return {
    passthroughFileCopy: true,
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes", // La cartella è RELATIVA all'input
    },
  };
};