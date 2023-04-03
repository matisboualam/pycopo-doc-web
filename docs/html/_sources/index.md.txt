---
myst:
  html_meta:
    "description lang=en": |
      Top-level documentation for pycopo library, with links to the rest
      of the site..
html_theme.sidebar_secondary.remove: true
---

<style>
      canvas {
        position: absolute;
        top: 10px;
        right: 55px;
        z-index: 0;
        background-color: transparent;
      }
</style>


# The Pycopo Sphinx Documentation
  
<br>



**PYCOPO** is a Python library based on the [aruco detection system](https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html) which aims to detect and locate <br> an object by monocular vision. 


```{note}
(*In this documentation, the term composite will refer to the object we want to track*)
```

This library has been created in the context of the development of a tridimensionnal localisation system by monocular vision in order to provide an assistance to the shoulder surgical navigation. 

**In this Sphinx doc, you'll find:**

- the **environment's configuration** required to run the diferent functions from pycopo modules
- a bit of the **theory** behind the pycopo method *(pinhole camera model, pose_estimation, composite defintion, etc..)*
- the complete **dictionnary** with each function shortly described and inputs, outputs specified
- an **exemple** showing the range of pycopo abilities
- a **small set of examples** illustrating the principals functions


## Installation Guide

Information about pycopo environment installation using dockerhub.

```{toctree}
:maxdepth: 2

usage
```

## Pycopo Theory

A brieve explanation of the concepts employed behind the pycopo library. 

```{toctree}
:maxdepth: 2

pycopo_theory
```

## Dictionnary

You will find in this section every function and Class definition with a short descritpion of its usage, the list of inputs required and the output type.

```{toctree}
:maxdepth: 2

modules
```

## Example

A complete Jupyter Notebook illustrating the range capacity and usage of the Pycopo modules.

```{toctree}

tutorial.ipynb
```

```{seealso}
- [gitlab repo](https://gitlab.com/symmehub/pycopo)
- [SYMME website](https://www.univ-smb.fr/symme/)
```

<div>
    <script async src="https://unpkg.com/es-module-shims@1.6.3/dist/es-module-shims.js"></script>
      <script type="importmap">
        {
          "imports": {
            "three": "https://unpkg.com/three@v0.151.0/build/three.module.js",
            "addons": "https://unpkg.com/three@v0.151.0/examples/jsm/loaders/GLTFLoader.js"
          }
        }
      </script>
      <script class="animation" type="module">
        import * as THREE from 'three';
        import { GLTFLoader } from 'addons';
        const scene = new THREE.Scene();
        const renderer = new THREE.WebGLRenderer( { antialias: true } );
        renderer.setPixelRatio( window.devicePixelRatio );
        const size = 400;
        renderer.setSize( size, size );
        renderer.outputEncoding = THREE.sRGBEncoding;
        document.body.appendChild( renderer.domElement );
        renderer.setClearColor(0x000000, 0);
        const camera = new THREE.PerspectiveCamera( 50, 1, 0.01, 1000 );
        camera.position.set( -10, 0.1, 0 );
        camera.rotation.set( -90, -90, -90 );
        camera.lookAt( 0, 0, 1 );
        const loader = new GLTFLoader();
        const pmremGenerator = new THREE.PMREMGenerator(renderer);
        loader.load( '_images/scene.glb', function ( gltf ) {
            gltf.scene.traverse(function (child) {
            // Check if this object is a mesh
            if (child.isMesh) {
            child.material = new THREE.MeshNormalMaterial();
            }
            });
            const model = gltf.scene.children[0];;
            model.position.set( 0, 0, 0 );
            model.rotation.set( -89.5, 0, 0 );
            const model_scale = 0.04;
            model.scale.set(model_scale, model_scale, model_scale);
            scene.add( model );
            const greenMaterial = new THREE.LineBasicMaterial( { color: 0x00ff00 } );
            const redMaterial = new THREE.LineBasicMaterial( { color: 0xff0000 } );
            const blueMaterial = new THREE.LineBasicMaterial( { color: 0x0000ff } );
            const greenPoints = [];
            const redPoints = [];
            const bluePoints = [];
            const line_scale = 0.7;
            greenPoints.push( new THREE.Vector3( 0, 0, 0 ) );
            greenPoints.push( new THREE.Vector3( -line_scale, 0, 0 ) );
            redPoints.push( new THREE.Vector3( 0, 0, 0 ) );
            redPoints.push( new THREE.Vector3( 0, -line_scale, 0 ) );
            bluePoints.push( new THREE.Vector3( 0, 0, 0 ) );
            bluePoints.push( new THREE.Vector3( 0, 0, -line_scale) );
            const greengeometry = new THREE.BufferGeometry().setFromPoints( greenPoints );
            const redgeometry = new THREE.BufferGeometry().setFromPoints( redPoints );
            const bluegeometry = new THREE.BufferGeometry().setFromPoints( bluePoints );
            const greenLine = new THREE.Line( greengeometry, greenMaterial );
            const redLine = new THREE.Line( redgeometry, redMaterial );
            const blueLine = new THREE.Line( bluegeometry, blueMaterial );
            const x_speed = 0.5;
            greenLine.rotation.x += x_speed;
            redLine.rotation.x += x_speed;
            blueLine.rotation.x += x_speed;
            model.rotation.x += x_speed;
            scene.add(greenLine);
            scene.add(redLine);
            scene.add(blueLine);
            function updateRotation() {
              const y_speed = 0.005;
              greenLine.rotation.y += y_speed;
              redLine.rotation.y += y_speed;
              blueLine.rotation.y += y_speed;
              model.rotation.z += y_speed;
              // greenLine.rotation.z += 0.01;
              // redLine.rotation.z += 0.01;
              // blueLine.rotation.z += 0.01;
              // model.rotation.y += 0.01;
            }
            function render() {
              updateRotation();
              renderer.render(scene, camera);
              requestAnimationFrame(render);
            }
            // Start the animation
            requestAnimationFrame(render);
          }, undefined, function ( error ) {
          console.error( error );} );
        renderer.render( scene, camera );
      </script>
  </div>
