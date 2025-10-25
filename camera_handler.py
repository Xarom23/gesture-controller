#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# Camera Handler - Clase para capturar video de la cámara y mostrarlo en un canvas

import cv2
from PIL import Image, ImageTk
import tkinter as tk
import mediapipe as mp
from landmark_detector import LandmarkDetector
from gesture_controller import GestureController


class CameraHandler:
    def __init__(self, canvas, camera_index=0, width=600, height=351):
        """
        Inicializa el manejador de cámara

        Args:
            canvas: El widget Canvas de tkinter donde se mostrará el video
            camera_index: Índice de la cámara (0 por defecto para la cámara principal)
            width: Ancho del frame
            height: Alto del frame
        """
        self.canvas = canvas
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap = None
        self.is_running = False
        self.show_video = True  # Controla si se muestra el video en el canvas
        self.show_landmarks = False  # Controla si se dibujan los landmarks
        self.delay = 15  # Delay en ms entre frames (aproximadamente 60 FPS)

        # Inicializar el detector de landmarks
        self.landmark_detector = LandmarkDetector(
            detect_hands=True,
            detect_face=True,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Utilidades de dibujo de MediaPipe
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.mp_face_mesh = mp.solutions.face_mesh
        
        # Inicializar el controlador de gestos
        self.gesture_controller = GestureController()

    def start(self):
        """Inicia la captura de video de la cámara"""
        if not self.is_running:
            self.cap = cv2.VideoCapture(self.camera_index)

            # Configurar resolución de la cámara
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            if self.cap.isOpened():
                self.is_running = True
                self._update_frame()
            else:
                raise Exception(f"No se pudo abrir la cámara {self.camera_index}")

    def stop(self):
        """Detiene la captura de video y libera la cámara"""
        self.is_running = False
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def set_show_video(self, show):
        """
        Controla si se debe mostrar el video en el canvas

        Args:
            show: True para mostrar el video, False para no actualizar el canvas
        """
        self.show_video = show

    def set_show_landmarks(self, show):
        """
        Controla si se deben dibujar los landmarks en el video

        Args:
            show: True para mostrar los landmarks, False para ocultarlos
        """
        self.show_landmarks = show

    def _update_frame(self):
        """Método privado que actualiza el frame en el canvas"""
        if self.is_running and self.cap is not None:
            # Solo capturar y mostrar el frame si show_video está activado
            if self.show_video:
                ret, frame = self.cap.read()

                if ret:
                    frame = cv2.flip(frame, 1)
                    # Convertir de BGR (OpenCV) a RGB para MediaPipe
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Detectar landmarks de manos y rostro
                    detection_results = self.landmark_detector.detect_landmarks(frame_rgb)

                    # Procesar gestos de manos si hay detecciones y el control gestual está activado
                    from config import gesture_control_enabled
                    if detection_results.hands and gesture_control_enabled:
                        self.gesture_controller.process_hand_gestures(detection_results.hands)

                    # Detectar landmarks si está activado
                    if self.show_landmarks:
                        # Dibujar landmarks de manos
                        if detection_results.hands and detection_results.hands.landmarks:
                            for hand_side, hand_landmarks in detection_results.hands.landmarks.items():
                                self.mp_drawing.draw_landmarks(
                                    frame_rgb,
                                    hand_landmarks,
                                    self.mp_hands.HAND_CONNECTIONS,
                                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                    self.mp_drawing_styles.get_default_hand_connections_style()
                                )

                        # Dibujar landmarks de rostro
                        if detection_results.face and detection_results.face.landmarks:
                            for face_idx, face_landmarks in detection_results.face.landmarks.items():
                                self.mp_drawing.draw_landmarks(
                                    frame_rgb,
                                    face_landmarks,
                                    self.mp_face_mesh.FACEMESH_TESSELATION,
                                    landmark_drawing_spec=None,
                                    connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style()
                                )
                                
    

                    # Redimensionar el frame si es necesario
                    frame_resized = cv2.resize(frame_rgb, (self.width, self.height))

                    # Convertir a formato PIL Image
                    img = Image.fromarray(frame_resized)

                    # Convertir a PhotoImage para tkinter
                    self.photo = ImageTk.PhotoImage(image=img)

                    # Limpiar el canvas y mostrar la nueva imagen
                    self.canvas.delete("all")
                    self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            # Programar la próxima actualización (siempre, aunque no se muestre)
            self.canvas.after(self.delay, self._update_frame)

    def get_current_frame(self):
        """
        Obtiene el frame actual sin mostrarlo en el canvas

        Returns:
            numpy.ndarray: Frame actual en formato BGR (OpenCV)
        """
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def set_camera(self, camera_index):
        """
        Cambia la cámara activa

        Args:
            camera_index: Índice de la nueva cámara
        """
        was_running = self.is_running
        if was_running:
            self.stop()

        self.camera_index = camera_index

        if was_running:
            self.start()

    def __del__(self):
        """Destructor para asegurar que la cámara se libere"""
        self.stop()
        # Cerrar el detector de landmarks
        if hasattr(self, 'landmark_detector'):
            self.landmark_detector.close()
