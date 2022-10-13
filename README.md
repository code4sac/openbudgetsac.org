# Open Budget: Sacramento

## Contributing

If you're looking for a starter development task to get your feet wet with our codebase, any of our Issues tagged [help wanted](https://github.com/code4sac/openbudgetsac.org/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) might be a good fit.

Some of the other Issues are larger and require some deeper design or architectural work; if one of those catches your eye, you'll probably want to talk with us for some more context and background. Either comment on the Issue or — even better — catch up with us at one of [Code for Sacramento's weekly Hack Nights](https://codeforsacramento.org/).

## Developing Locally

### Quick Start Guide for Unix-based systems (Mac or Linux)

1. Sign into GitHub and fork this repo
1. Clone the fork onto your machine and navigate to the new folder
1. While still in the root directory of the repo, create a new folder called "build". This folder will be ignored by our version control system.
1. Navigate to the \_src/ folder, which is where all development work takes place.
1. Install dependencies with `npm install`
1. Serve the website by entering `npx @11ty/eleventy --serve --port=8011`

Congratulations! Your local copy of Open Budget Sacramento's website should now be running at http://localhost:8011. That means you're ready to do the codez if you want to contribute to the codebase of Open Budget Sacramento. You will probably want to open a new terminal window, though, to regain access to the command line.

- Please note that after editing a SASS file you should run `npm run build-css` from the \_src/ folder in order to incorporate your changes into the CSS

### Eleventy

This site is built with [Eleventy](https://11ty.dev), a JavaScript-based static site generator that parses Markdown, Pug, and other template languages and runs on Node.js. That means you can reproduce our site locally with minimal setup!

You'll need these installed globally:

- [Node](http://nodejs.org/download/) is a prerequisite for NPM
- [NPM](https://npmjs.com) or [Yarn](https://yarnpkg.com/en/)
- [NVM](https://github.com/nvm-sh/nvm/blob/master/README.md) is optional, but very handy for downloading, updating, and switching between versions of NPM

### Install & Run Eleventy in \_src/

Once you have the NPM package manager installed, you can install Eleventy and the other dependencies listed in **package.json**. Enter the following from the \_src/ folder, where the Eleventy configuration file **.eleventy.js** lives.

```
npm install
```

This command usually runs without a glitch, but if you run into trouble, check your version of node. The latest version of node that we can confirm works with our set-up is **v15.14.0**.

To start Eleventy, simply enter the following. (You may choose any network port on your system that is available; 8011 is just a suggestion.)

```
npx @11ty/eleventy --serve --port=8011
```

## Frontend Stack

This project is coded with, among other things:

- [Bootstrap](http://getbootstrap.com/), a CSS framework
- [D3](https://d3js.org), a data visualization library for JavaScript
- [Pug](https://pugjs.org/api/getting-started.html), a JavaScript-friendly HTML templating language
- [React](https://facebook.github.io/react/), a rendering library for JavaScript
- [Sass](https://sass-lang.com/), a CSS preprocessor

## Creating & Editing Pages

- Please note that it is your responsibility to keep your fork of the repo up-to-date with changes made by others working on the project. Doing this diligently should go a long way towards protecting you from scary git merge conflicts.
- All development activity occurs in `_src/`. The root folder is only for compiled output for deployment.
- Page content is inserted into the `content` block. If you are updating data, be sure you understand how it will be consumed.
- In many cases you will simply create or update a `.pug` file, which Eleventy will turn into HTML. If you are making another type of change, you may need to read Pug documentation (which is excellent, by the way!).
- If your page uses custom page-specific css, add it to a new `.scss` partial and import it into the main stylesheet. (Make sure to namespace it the same way the others are.)

### Additional instructions for "flow" diagram pages

1. Flow pages are built off a template; copy one of the `*-budget-flow.pug` pages and update the content blocks as necessary.
1. Data files must be placed in the `data/flow` directory. Follow the naming convention seen there or your files won't load properly. You also will need to point your page at the appropriate files as seen in the `get_datafiles` content block.
1. the following columns are required in your datafile and their names should be normalized as seen here. Other columns should be removed to minimize the data download.
   - budget_year
   - department
   - fund_code
   - account_type (this should be the Expense/Revenue column, if there are duplicate names)
   - account_category
   - amount

### Additional instructions for treemap diagram pages

1. Treemap pages are built off a template; copy one of the `*-budget-tree.pug` pages and update the content blocks as necessary.
1. Instructions for generating the necessary data files can be found [here](_treemap/README.md). Add them to the `data/tree/` directory following the naming convention seen in the existing files.
1. Update the `datafiles` content block with the appropriate metadata and file path for the data files you generated.

### Additional instructions for the Compare page

1. The Compare page is a React application. The source files are in `_src/js/compare/` and are are bundled with [Webpack](https://webpack.js.org/).
1. When developing on the Compare page, run `yarn` to install all the necessary node dependencies and `yarn run watch` to watch the source files for changes and rebuild the asset bundles accordingly.

## Publishing Changes

Make changes and review them on your local development site. If everything looks good, push your changes to your personal fork and merge the commit(s) into your master branch. Finally, issue a pull request and we'll take it from there!

### Issuing a pull request

Simply push your code changes to your repo in whatever branch you used locally, then merge into master. At this point you can either 1) push from your master to the **staging** branch of the upstream repo or 2) just tell an admin of the upstream repo that your work is ready for review. (Anyone with admin privileges on the original repo will be able to create a pull request from your repo). Your changes will then be reviewed, tested, and (if everything looks good) pushed into the master branch.

Starting in March 2020, code changes pushed to the master branch of the (original) repo will use GitHub Actions to trigger a continuous integration process that (among other things):

- runs WebPack;
- builds static files with Eleventy; and
- deploys the updated web files to GitHub Pages
