import time

class PID:
    def __init__(self, Kp, Ki, Kd, setpoint, sample_time=0.01):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.setpoint = setpoint  # Desired setpoint
        self.sample_time = sample_time  # Time interval between PID updates

        self.prev_error = 0  # Previous error for derivative calculation
        self.integral = 0  # Integral term accumulator
        self.last_time = time.time()  # Time of the last update

    def update(self, current_value):
        error = self.setpoint - current_value  # Calculate the error
        current_time = time.time()  # Get the current time
        dt = current_time - self.last_time  # Calculate the time delta

        # Only update if the sample time has passed
        if dt >= self.sample_time:
            proportional = self.Kp * error  # Calculate proportional term
            self.integral += error * dt  # Update integral accumulator
            derivative = self.Kd * (error - self.prev_error) / dt  # Calculate derivative term

            self.prev_error = error  # Update previous error
            self.last_time = current_time  # Update last time

            # Return the sum of the proportional, integral, and derivative terms
            return proportional + self.integral * self.Ki + derivative
        return 0

# Ziegler-Nichols tuning method implementation
def ziegler_nichols_tuning(pid, process, step_size=0.1, oscillation_threshold=0.01):
    pid.Kp += step_size  # Increase the Kp value by step_size
    last_output = process(0)  # Get the initial output from the process
    oscillations = 0  # Count the number of oscillations
    increasing = True  # Flag to track if the output is increasing or not

    # Iterate until the output oscillates around the setpoint
    while True:
        # Update the PID controller and get the new output
        output = pid.update(process(pid.update(0)))

        # Check if the output has stopped changing
        if abs(output - last_output) < oscillation_threshold:
            break

        # Count oscillations and update the increasing flag
        if output > last_output:
            if not increasing:
                oscillations += 1
                increasing = True
        else:
            increasing = False

        last_output = output  # Update the last output
        pid.Kp += step_size  # Increase the Kp value by step_size

    # Calculate the ultimate gain (Ku) and period (Tu)
    Ku = pid.Kp
    Tu = 2 * step_size * oscillations

    # Set the tuned PID parameters using the Ziegler-Nichols method
    pid.Kp = 0.6 * Ku
    pid.Ki = 1.2 * Ku / Tu
    pid.Kd = 3 * Ku * Tu / 40

# Usage example
def dummy_process(value):
    return value * 2

if __name__ == "__main__":
    pid = PID(0.0, 0.0, 0.0, 1.0)
    ziegler_nichols_tuning(pid, dummy_process)
    
    print(f"Tuned PID parameters: Kp={pid.Kp}, Ki={pid.Ki}, Kd={pid.Kd}")

