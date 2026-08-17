import tensorflow as tf

model = tf.keras.models.load_model("DeepShield_CNN.keras")

print("\nModel Built:", model.built)

try:
    print("\nModel Input:", model.input)
except Exception as e:
    print("\nModel Input Error:", e)

dummy = tf.random.normal((1,224,224,3))

print("\nRunning one forward pass...")
output = model(dummy)

print("Output shape:", output.shape)

print("\nAfter forward pass:")

try:
    print("Model Input:", model.input)
except Exception as e:
    print("Still Error:", e)

print("\nLayer names:")

for layer in model.layers:
    print(layer.name)