import tkinter as tk
from tkinter import ttk
import math

class GeodesyConverterGUI:
    def __init__(self, root):
        self.root = root
        root.title("Geodesy Coordinate Converter")

        # Ellipsoid parameters (GRS-80 as default)
        self.a_var = tk.StringVar(value="6378137.0000")
        self.b_var = tk.StringVar(value="6356752.3141")

        # Geodetic coordinates
        self.lat_deg_var = tk.StringVar(value="47")
        self.lon_deg_var = tk.StringVar(value="15")
        self.h_var = tk.StringVar(value="2000")

        # ECEF coordinates
        self.x_var = tk.StringVar()
        self.y_var = tk.StringVar()
        self.z_var = tk.StringVar()

        # Geodetic output coordinates (for inverse)
        self.lat_out_deg_var = tk.StringVar()
        self.lon_out_deg_var = tk.StringVar()
        self.h_out_var = tk.StringVar()

        # --- Input Frame ---
        input_frame = ttk.Frame(root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(input_frame, text="Ellipsoid Parameters (GRS-80):").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(input_frame, text="Semi-major axis (a):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.a_var, width=15).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(input_frame, text="Semi-minor axis (b):").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.b_var, width=15).grid(row=2, column=1, sticky=tk.W)

        ttk.Label(input_frame, text="Geodetic Coordinates:").grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Label(input_frame, text="Latitude (φ) [deg]:").grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.lat_deg_var, width=10).grid(row=4, column=1, sticky=tk.W)
        ttk.Label(input_frame, text="Longitude (λ) [deg]:").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.lon_deg_var, width=10).grid(row=5, column=1, sticky=tk.W)
        ttk.Label(input_frame, text="Height (h) [m]:").grid(row=6, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.h_var, width=10).grid(row=6, column=1, sticky=tk.W)

        # --- Button Frame ---
        button_frame = ttk.Frame(root, padding="10")
        button_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))

        ttk.Button(button_frame, text="Forward Transform (Geodetic to ECEF)", command=self.forward_transform).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Inverse Transform (ECEF to Geodetic)", command=self.inverse_transform).grid(row=0, column=1, padx=5)


        # --- Output Frame ---
        output_frame = ttk.Frame(root, padding="10")
        output_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(output_frame, text="ECEF Coordinates:").grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(output_frame, text="X [m]:").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.x_var).grid(row=1, column=1, sticky=tk.W)
        ttk.Label(output_frame, text="Y [m]:").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.y_var).grid(row=2, column=1, sticky=tk.W)
        ttk.Label(output_frame, text="Z [m]:").grid(row=3, column=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.z_var).grid(row=3, column=1, sticky=tk.W)

        ttk.Label(output_frame, text="Geodetic Coordinates (Inverse):").grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Label(output_frame, text="Latitude (φ) [deg]:").grid(row=5, column=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.lat_out_deg_var).grid(row=5, column=1, sticky=tk.W)
        ttk.Label(output_frame, text="Longitude (λ) [deg]:").grid(row=6, column=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.lon_out_deg_var).grid(row=6, column=1, sticky=tk.W)
        ttk.Label(output_frame, text="Height (h) [m]:").grid(row=7, column=0, sticky=tk.W)
        ttk.Label(output_frame, textvariable=self.h_out_var).grid(row=7, column=1, sticky=tk.W)

        for child in input_frame.winfo_children():
            child.grid_configure(padx=5, pady=2)
        for child in button_frame.winfo_children():
            child.grid_configure(padx=5, pady=5)
        for child in output_frame.winfo_children():
            child.grid_configure(padx=5, pady=2)

    def forward_transform(self):
        try:
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            lat_deg = float(self.lat_deg_var.get())
            lon_deg = float(self.lon_deg_var.get())
            h = float(self.h_var.get())

            lat_rad = math.radians(lat_deg)
            lon_rad = math.radians(lon_deg)
            e2 = (a**2 - b**2) / a**2
            N = a / math.sqrt(1 - e2 * math.sin(lat_rad)**2)

            X = (N + h) * math.cos(lat_rad) * math.cos(lon_rad)
            Y = (N + h) * math.cos(lat_rad) * math.sin(lon_rad)
            Z = (N * (1 - e2) + h) * math.sin(lat_rad)

            self.x_var.set(f"{X:.3f}")
            self.y_var.set(f"{Y:.3f}")
            self.z_var.set(f"{Z:.3f}")

        except ValueError:
            self.x_var.set("Invalid Input")
            self.y_var.set("Invalid Input")
            self.z_var.set("Invalid Input")

    def inverse_transform(self):
        try:
            a = float(self.a_var.get())
            b = float(self.b_var.get())
            X = float(self.x_var.get())
            Y = float(self.y_var.get())
            Z = float(self.z_var.get())

            e2 = (a**2 - b**2) / a**2
            p = math.sqrt(X**2 + Y**2)
            lat_rad_prev = math.atan2(Z, p)
            lat_rad = 0
            h = 0

            for _ in range(10): # Iterative refinement - fixed number of iterations
                N = a / math.sqrt(1 - e2 * math.sin(lat_rad_prev)**2)
                h = p / math.cos(lat_rad_prev) - N
                lat_rad = math.atan2(Z, p * (1 - e2 * N / (N + h)))
                if abs(lat_rad - lat_rad_prev) < 1e-9: # Convergence check (optional, using fixed iterations for simplicity)
                    break
                lat_rad_prev = lat_rad


            lon_rad = math.atan2(Y, X)
            lat_deg = math.degrees(lat_rad)
            lon_deg = math.degrees(lon_rad)

            self.lat_out_deg_var.set(f"{lat_deg:.6f}")
            self.lon_out_deg_var.set(f"{lon_deg:.6f}")
            self.h_out_var.set(f"{h:.3f}")

        except ValueError:
            self.lat_out_deg_var.set("Invalid ECEF Input")
            self.lon_out_deg_var.set("Invalid ECEF Input")
            self.h_out_var.set("Invalid ECEF Input")


if __name__ == "__main__":
    root = tk.Tk()
    gui = GeodesyConverterGUI(root)
    root.mainloop()