import babel from 'rollup-plugin-babel';
import nodeResolve from 'rollup-plugin-node-resolve';
import commonjs from 'rollup-plugin-commonjs';
import replace from 'rollup-plugin-replace';
import uglify from 'rollup-plugin-uglify';

export default {
  entry: 'src/main.js',
  format: 'umd',
  plugins: [
    babel({
      presets: [
        "es2015-rollup",
        "stage-0",
        "react"
      ],
      exclude: 'node_modules/**'
    }),
    nodeResolve({
      jsnext: true,
      main: true,
      browser: true
    }),
    commonjs({
      include: 'node_modules/**'
    }),
    replace({
      'process.env.NODE_ENV': JSON.stringify( 'production' )
    }),
    uglify()
  ],
  dest: 'static/js/bundle.js'
};
