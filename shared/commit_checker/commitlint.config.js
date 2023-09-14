module.exports = {
  extends: [
    // https://github.com/conventional-changelog/commitlint/tree/a90ffe98bc4abe16a353f836927d2f8867797080/%40commitlint/config-conventional
    "@commitlint/config-conventional",
  ],
  // https://commitlint.js.org/#/reference-rules
  // What are the elements presented in a conventional commit:
  // type(scope?): subject
  // body?
  // footer?
  rules: {
    "body-leading-blank": [2, "always"],
    "subject-case": [2, "always", ["lower-case"]],
    "header-max-length": [2, "always", 72],
  },
};
