# Troodon v2 350mm Configuration

This configuration is specifically designed for the Troodon v2 350mm printer, which aims to enhance its performance, reliability, and print quality through carefully selected hardware and firmware modifications.

## Hardware Components

- **Mainboard**: Octopus X7 (A clone from Octopus Pro v1.1) - Offers extensive control capabilities for managing a wide range of sensors and accessories, ensuring a versatile and powerful 3D printing setup.
- **Extruder**: StealthBurner CW2 - An updated version of the StealthBurner, featuring improved cooling and reduced noise for a better printing experience.
- **Hotend**: E3D V6 Hotend - Renowned for its reliability and adaptability, the E3D V6 is capable of printing a diverse array of materials with ease.

## Firmware Note

The Troodon v2 350mm comes pre-installed with Klipper firmware, known for its high performance and flexibility. However, it does not include Klippain by default. Our provided configuration files are based on Klippain, a customized version of Klipper that introduces additional features and optimizations for an even better printing experience.

To utilize these configurations, you'll need to replace the standard Klipper firmware with Klippain. These files were crafted starting from the `printer.cfg` file to ensure compatibility and performance with the Troodon v2 350mm, incorporating Klippain's advanced features and capabilities.

### Transitioning to Klippain

1. **Installation**: Follow the [Klippain installation instructions](https://github.com/Frix-x/klippain#installation) to install Klippain on your Troodon.
2. **Configuration Adaptation**: Our Klippain configuration files serve as a comprehensive starting point, derived from the initial `printer.cfg`. You might need to adjust settings according to your specific modifications or preferences.
3. **Testing and Tuning**: After installation, thoroughly test and fine-tune your setup to ensure optimal performance and safety.

## Notes on Configuration

This configuration is intended as a guideline to enhance your Troodon v2 350mm with the capabilities of Klippain. It is crucial to review and understand each setting's impact, gradually test modifications, and consult community resources for guidance.

Please be aware that changing firmware and hardware configurations can significantly affect your printer's behavior. Proceed with caution and always prioritize safety in your modifications.

## Contributing

Contributions to refine and expand this configuration are welcome. If you've made improvements or have suggestions, please share them with the community by submitting a pull request or creating an issue in this repository.
