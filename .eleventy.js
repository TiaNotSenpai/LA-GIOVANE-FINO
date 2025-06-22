module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/css");
  eleventyConfig.addPassthroughCopy("src/js");
  eleventyConfig.addPassthroughCopy("src/images");
  eleventyConfig.addPassthroughCopy("src/admin");

  return {
    passthroughFileCopy: true,
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes", // L'unica cosa che conta per i layout
    },
  };
};