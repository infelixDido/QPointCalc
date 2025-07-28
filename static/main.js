const cameraControls = {
  real: {
    radius: 10,
    theta: Math.PI / 4,
    phi: Math.PI / 4,
    isDragging: false,
    previousMousePosition: { x: 0, y: 0 },
    rotationSpeed: 0.005
  },
  reciprocal: { 
    isDragging: false, 
    previousMousePosition: { x: 0, y: 0 }, 
    rotationSpeed: 0.01,
    radius: 5,
    theta: Math.PI / 2,
    phi: Math.PI / 2
  }
};

function setupCameraControls(type, canvas, camera) {
  const controls = cameraControls[type];

  const updateCameraPosition = () => {
    const radius = controls.radius;
    const theta = controls.theta;
    const phi = controls.phi;

    camera.position.x = radius * Math.sin(phi) * Math.cos(theta);
    camera.position.y = radius * Math.cos(phi);
    camera.position.z = radius * Math.sin(phi) * Math.sin(theta);

    camera.lookAt(0, 0, 0);
  };

  updateCameraPosition();

  canvas.addEventListener('mousedown', (event) => {
    controls.isDragging = true;
    controls.previousMousePosition = { x: event.clientX, y: event.clientY };
  });

  canvas.addEventListener('mousemove', (event) => {
    if (!controls.isDragging) return;

    const dx = event.clientX - controls.previousMousePosition.x;
    const dy = event.clientY - controls.previousMousePosition.y;

    controls.theta += dx * controls.rotationSpeed;
    controls.phi = Math.max(0.1, Math.min(Math.PI - 0.1, controls.phi - dy * controls.rotationSpeed));

    updateCameraPosition();
    controls.previousMousePosition = { x: event.clientX, y: event.clientY };
  });

  canvas.addEventListener('mouseup', () => {
    controls.isDragging = false;
  });

  canvas.addEventListener('wheel', (event) => {
    event.preventDefault();
    controls.radius += event.deltaY > 0 ? 0.1 : -0.1;
    controls.radius = Math.max(2, Math.min(15, controls.radius));
    updateCameraPosition();
  }, { passive: false });
}

function renderLatticeScene(lattice, containerId = "lattice-plot", color = 0xff0000, latticeType = "real") {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  
  const renderer = new THREE.WebGLRenderer();
  renderer.setSize(container.clientWidth, container.clientHeight);
  container.appendChild(renderer.domElement);

  const scene = new THREE.Scene();

  const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
  setupCameraControls(latticeType, renderer.domElement, camera);
  
  const axesHelper = new THREE.AxesHelper(5);
  scene.add(axesHelper);

  function drawLatticeCell(vectors, color, repeats = 1) {
    const [a, b, c] = vectors.map(v => new THREE.Vector3(...v));

    const solidMaterial = new THREE.LineBasicMaterial({ color, opacity: 0.7, transparent: true });
    const sphereGeometry = new THREE.SphereGeometry(0.1, 16, 16);
    const sphereMaterial = new THREE.MeshBasicMaterial({ color });

    const baseCell = new THREE.Group();

    const origin = new THREE.Vector3(0, 0, 0);
    const A = a.clone();
    const B = b.clone();
    const C = c.clone();
    const AB = a.clone().add(b);
    const AC = a.clone().add(c);
    const BC = b.clone().add(c);
    const ABC = a.clone().add(b).add(c);

    const solidEdges = [
      [origin, A], [origin, B], [origin, C],
      [A, AB], [A, AC],
      [B, AB], [B, BC],
      [C, AC], [C, BC],
      [AB, ABC], [AC, ABC], [BC, ABC]
    ];

    solidEdges.forEach(([start, end]) => {
      const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);
      const line = new THREE.Line(geometry, solidMaterial);
      baseCell.add(line);
    });

    [A, B, C].forEach(vec => {
      const dot = new THREE.Mesh(sphereGeometry, sphereMaterial);
      dot.position.copy(vec);
      baseCell.add(dot);
    });

    /*const isHexagonal = angles &&
      Math.abs(angles[0] - 90) < 1e-2 &&
      Math.abs(angles[1] - 90) < 1e-2 &&
      Math.abs(angles[2] - 120) < 1e-2;

    console.log("Is hexagonal:", isHexagonal);*/
    
    for (let i = 0; i < 3; i++) {
      const angle = (i * 2 * Math.PI) / 3;  // 0, 120, 240 degrees
      const instance = baseCell.clone();
      instance.rotateZ(angle); // rotate around z (c axis)
      scene.add(instance);
    }
    /*
    for (let i = 0; i < repeats; i++) {
        const cellInstance = baseCell.clone();
        const offset = a.clone().multiplyScalar(i);
        cellInstance.position.copy(offset);
        scene.add(cellInstance);
      }
    */
  }

  /*
  function drawVector(v, color) {
    const geometry = new THREE.BufferGeometry().setFromPoints([
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(...v)
    ]);
    const mat = new THREE.LineBasicMaterial({ color });
    const line = new THREE.Line(geometry, mat);
    scene.add(line);

    // Add a dot at the end
    const sphereGeometry = new THREE.SphereGeometry(0.2, 16, 16);
    const sphereMaterial = new THREE.MeshBasicMaterial({ color });
    const dot = new THREE.Mesh(sphereGeometry, sphereMaterial);
    dot.position.set(...v);
    scene.add(dot);
  }
  */
  drawLatticeCell(lattice, color, 2);

  function animate() {
    requestAnimationFrame( animate );
    renderer.render(scene, camera);
  }

  animate();
}

async function submitForm() {
    // validate inputs
    try {
        two_theta = JSON.parse(document.getElementById("two_theta").value);
        u = JSON.parse(document.getElementById("u").value);
        v = JSON.parse(document.getElementById("v").value);
        r = JSON.parse(document.getElementById("r").value);
        w = JSON.parse(document.getElementById("w").value);
        if (!Array.isArray(u) || u.length !== 3 || !u.every(Number.isFinite)) throw "Invalid u";
        if (!Array.isArray(v) || v.length !== 3 || !v.every(Number.isFinite)) throw "Invalid v";
        if (!Array.isArray(r) || r.length !== 3 || !r.every(Number.isFinite)) throw "Invalid r";
        if (!Array.isArray(w) || w.length !== 3 || !w.every(Number.isFinite)) throw "Invalid w";

        if (!Array.isArray(two_theta) || !two_theta.every(Number.isFinite)) throw "Invalid two_theta";
    } catch (err) {
        alert("Please enter valid vectors like [1, 0, 0]");
        return;
    }

    const data = {
      param1: document.getElementById("param1").value,
      param2: document.getElementById("param2").value,
      param3: document.getElementById("param3").value,
      param4: document.getElementById("param4").value,
      param5: document.getElementById("param5").value,
      param6: document.getElementById("param6").value,
      param7: document.getElementById("param7").value,
      two_theta: two_theta,
      u: u,
      v: v,
      r: r,
      w: w,
    };

    const response = await fetch("/calculate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    
    document.getElementById("lat_info").innerHTML = `
      <pre>
        Lattice: ${result.lattice}
        Reciprocal: ${result.reciprocal_lattice}
        Angle between ${u} and ${v}: ${result.angle.toFixed(3)}°
      </pre>
    `;

    document.getElementById("angle_info").innerHTML = `
      <pre>
        Angle between ${u} and ${v}: ${result.angle.toFixed(3)}°
      </pre>
    `;

    const thetaCut = result.theta_cut;

    if (thetaCut) {
      Plotly.newPlot("thetaCutPlot", thetaCut.traces, thetaCut.layout);
    } else {
      console.log("No theta_cut data returned.");
    }

    const lattice_visual = result.lattice_visual;

    const angles = [
      parseFloat(document.getElementById("param4").value),
      parseFloat(document.getElementById("param5").value),
      parseFloat(document.getElementById("param6").value),
    ];

    console.log("Lattice visual:", lattice_visual);
    console.log("Angles:", angles);
    
    if (lattice_visual) {
      renderLatticeScene(lattice_visual, "lattice-plot", 0xff0000, "real");
    }
    /*
    const reciprocal_lattice_visual = result.reciprocal_lattice_visual;
    if (reciprocal_lattice_visual) {
      renderLatticeScene(reciprocal_lattice_visual, "recip-lattice-plot", 0x0000ff, angles, "reciprocal");
    }
    */

    /*
    const Q = result.plot.Q;
    const omega = result.plot.omega;
    const thetaAngles = result.plot.theta_angles;

    const traces = thetaAngles.map((theta, i) => ({
        x: Q[i],
        y: omega,
        mode: 'lines',
        line: { dash: 'dot' },
        name: `2θ = ${Math.round(theta)}°`
    }));

    Plotly.newPlot("plot", traces, {
        title: "Dynamic Range Plot",
        xaxis: { title: 'Q (Å⁻¹)' },
        yaxis: { title: 'Energy Transfer (meV)' }
    });
    */
}
