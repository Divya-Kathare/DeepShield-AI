from utils.predictor import load_model
from utils.gradcam import generate_gradcam

# Load the model
model = load_model()

# Change this to the path of one test image
image_path = "test.jpg"

# Generate Grad-CAM
heatmap, overlay = generate_gradcam(image_path, model)

# Save the outputs
heatmap.save("heatmap.png")
overlay.save("overlay.png")

print("✅ Grad-CAM generated successfully!")
print("Saved:")
print(" - heatmap.png")
print(" - overlay.png")