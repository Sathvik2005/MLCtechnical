import * as THREE from 'three'

export function createWorldScene(container, world, onSelect) {
  const scene = new THREE.Scene()
  scene.background = new THREE.Color('#dbeafe')

  const camera = new THREE.PerspectiveCamera(75, container.clientWidth / container.clientHeight, 0.1, 1000)
  camera.position.set(0, 8, 16)

  const renderer = new THREE.WebGLRenderer({ antialias: true })
  renderer.setSize(container.clientWidth, container.clientHeight)
  container.appendChild(renderer.domElement)

  const hemi = new THREE.HemisphereLight(0xffffff, 0xb0c4de, 1.1)
  scene.add(hemi)

  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(160, 160),
    new THREE.MeshLambertMaterial({ color: '#bbf7d0' }),
  )
  ground.rotation.x = -Math.PI / 2
  scene.add(ground)

  const home = new THREE.Mesh(
    new THREE.BoxGeometry(world.home.size, world.home.size, world.home.size),
    new THREE.MeshStandardMaterial({ color: '#fef3c7', emissive: '#fde68a', emissiveIntensity: world.home.glow || 0.2 }),
  )
  home.position.set(0, world.home.size / 2, 0)
  home.userData = { type: 'home', payload: world.home }
  scene.add(home)

  world.buildings.forEach((b) => {
    const mesh = new THREE.Mesh(
      new THREE.BoxGeometry(b.size, b.height, b.size),
      new THREE.MeshStandardMaterial({ color: b.color }),
    )
    mesh.position.set(b.position.x, b.height / 2, b.position.z)
    mesh.userData = { type: 'repo', payload: b }
    scene.add(mesh)
  })

  world.trees.forEach((tree) => {
    const trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.3, 1.5), new THREE.MeshStandardMaterial({ color: '#7c5a3b' }))
    trunk.position.set(tree.x, 0.8, tree.z)
    scene.add(trunk)
    const leaves = new THREE.Mesh(new THREE.SphereGeometry(0.8), new THREE.MeshStandardMaterial({ color: '#16a34a' }))
    leaves.position.set(tree.x, 2, tree.z)
    scene.add(leaves)
  })

  const raycaster = new THREE.Raycaster()
  const mouse = new THREE.Vector2()
  const keys = {}

  function onKeyDown(e) { keys[e.key.toLowerCase()] = true }
  function onKeyUp(e) { keys[e.key.toLowerCase()] = false }
  function onClick(e) {
    const rect = renderer.domElement.getBoundingClientRect()
    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1
    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1
    raycaster.setFromCamera(mouse, camera)
    const hits = raycaster.intersectObjects(scene.children)
    if (hits[0]?.object?.userData?.type) onSelect(hits[0].object.userData)
  }

  window.addEventListener('keydown', onKeyDown)
  window.addEventListener('keyup', onKeyUp)
  renderer.domElement.addEventListener('click', onClick)

  function animate() {
    if (keys['w']) camera.position.z -= 0.2
    if (keys['s']) camera.position.z += 0.2
    if (keys['a']) camera.position.x -= 0.2
    if (keys['d']) camera.position.x += 0.2
    renderer.render(scene, camera)
    requestAnimationFrame(animate)
  }
  animate()

  return () => {
    window.removeEventListener('keydown', onKeyDown)
    window.removeEventListener('keyup', onKeyUp)
    renderer.domElement.removeEventListener('click', onClick)
    renderer.dispose()
    container.removeChild(renderer.domElement)
  }
}
