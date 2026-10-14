import tkinter as tk
from tkinter import messagebox, ttk
from backend.entity.cita import Cita

class AppVeterinaria:
    def __init__(self, root, cita_service, clinica_repo):
        self.root = root
        self.cita_service = cita_service
        self.clinica_repo = clinica_repo
        self.clinica_actual = None  
        
        self.root.title("Sistema de Gestión Veterinaria - Arquitectura Limpia")
        self.root.geometry("780x550")
        self.root.config(bg="#f4f7f9")
        
        self.frame_actual = None
        self.mostrar_login()

    def limpiar_ventana(self):
        if self.frame_actual:
            self.frame_actual.destroy()

    def mostrar_login(self):
        self.limpiar_ventana()
        self.frame_actual = tk.Frame(self.root, bg="#ffffff", padx=40, pady=40, relief="solid", bd=1)
        self.frame_actual.place(relx=0.5, rely=0.5, anchor="center", width=420, height=360)

        tk.Label(self.frame_actual, text="🐾 Portal Clínicas Veterinarias", font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#1b4f8a").pack(pady=15)

        tk.Label(self.frame_actual, text="NIT de la Clínica:", bg="#ffffff", anchor="w").pack(fill="x")
        self.entry_nit = tk.Entry(self.frame_actual, font=("Helvetica", 12))
        self.entry_nit.pack(fill="x", pady=5)
        self.entry_nit.insert(0, "901456789-1")  # Huellitas por defecto

        tk.Label(self.frame_actual, text="Contraseña:", bg="#ffffff", anchor="w").pack(fill="x", pady=(5,0))
        self.entry_pass = tk.Entry(self.frame_actual, show="*", font=("Helvetica", 12))
        self.entry_pass.pack(fill="x", pady=5)
        self.entry_pass.insert(0, "1234")

        tk.Button(self.frame_actual, text="Iniciar Sesión", bg="#1b4f8a", fg="white", font=("Helvetica", 11, "bold"), relief="flat", command=self.intentar_login).pack(fill="x", pady=20)

    def intentar_login(self):
        nit = self.entry_nit.get()
        password = self.entry_pass.get()
        
        clinica = self.clinica_repo.buscar_por_nit(nit)
        
        if clinica and clinica.password == password:
            self.clinica_actual = clinica
            self.mostrar_dashboard()
        else:
            messagebox.showerror("Error de Autenticación", "NIT o contraseña incorrectos.")

    def mostrar_dashboard(self):
        self.limpiar_ventana()
        self.frame_actual = tk.Frame(self.root, bg="#f4f7f9", padx=20, pady=20)
        self.frame_actual.pack(fill="both", expand=True)

        header = tk.Frame(self.frame_actual, bg="#1b4f8a", padx=15, pady=15)
        header.pack(fill="x", pady=(0, 20))
        tk.Label(header, text=f"🏢 {self.clinica_actual.nombre}", font=("Helvetica", 14, "bold"), bg="#1b4f8a", fg="white").pack(side="left")
        tk.Button(header, text="Cerrar Sesión", bg="#d9534f", fg="white", relief="flat", command=self.mostrar_login).pack(side="right")

        panel_acciones = tk.Frame(self.frame_actual, bg="#f4f7f9")
        panel_acciones.pack(fill="both", expand=True)

        tk.Button(panel_acciones, text="📅 Agendar Nueva Cita", bg="white", fg="#333", font=("Helvetica", 11, "bold"), height=2, width=30, relief="solid", bd=1, command=self.vista_agendar_cita).pack(pady=10)
        tk.Button(panel_acciones, text="❌ Cancelar Cita", bg="white", fg="#333", font=("Helvetica", 11), height=2, width=30, relief="solid", bd=1, command=self.vista_cancelar_cita).pack(pady=10)
        tk.Button(panel_acciones, text="🩺 Atender Cita y Facturar", bg="white", fg="#333", font=("Helvetica", 11), height=2, width=30, relief="solid", bd=1, command=self.vista_atender_cita).pack(pady=10)

    def vista_agendar_cita(self):
        ventana_agendar = tk.Toplevel(self.root)
        ventana_agendar.title("Agendar Nueva Cita")
        ventana_agendar.geometry("440x480")
        ventana_agendar.config(bg="#ffffff")

        tk.Label(ventana_agendar, text="📅 Programar Cita Médica", font=("Helvetica", 13, "bold"), bg="#ffffff", fg="#1b4f8a").pack(pady=15)

        siguiente_num = len(self.clinica_actual.citas) + 1
        codigo_sugerido = f"CIT-{siguiente_num:03d}"

        tk.Label(ventana_agendar, text="Código de Cita (Generado automáticamente):", bg="#ffffff", anchor="w").pack(fill="x", padx=30)
        entry_codigo = tk.Entry(ventana_agendar, font=("Helvetica", 11))
        entry_codigo.pack(fill="x", padx=30, pady=5)
        entry_codigo.insert(0, codigo_sugerido)

        tk.Label(ventana_agendar, text="Fecha (Ej. 11 de noviembre de 2026):", bg="#ffffff", anchor="w").pack(fill="x", padx=30)
        entry_fecha = tk.Entry(ventana_agendar, font=("Helvetica", 11))
        entry_fecha.pack(fill="x", padx=30, pady=5)
        entry_fecha.insert(0, "11 de noviembre de 2026")

        # Formato universal 24h limpio
        tk.Label(ventana_agendar, text="Hora Universal 24h (Ej. 09:00 o 14:30):", bg="#ffffff", anchor="w").pack(fill="x", padx=30)
        entry_hora = tk.Entry(ventana_agendar, font=("Helvetica", 11))
        entry_hora.pack(fill="x", padx=30, pady=5)
        entry_hora.insert(0, "09:00")

        tk.Label(ventana_agendar, text="Seleccione Mascota:", bg="#ffffff", anchor="w").pack(fill="x", padx=30)
        lista_mascotas_nombres = []
        mapa_mascotas = {}
        for prop in self.clinica_actual.propietarios:
            for m in prop.mascotas:
                texto = f"{m.nombre} ({prop.nombre})"
                lista_mascotas_nombres.append(texto)
                mapa_mascotas[texto] = m

        combo_mascotas = ttk.Combobox(ventana_agendar, values=lista_mascotas_nombres, state="readonly", font=("Helvetica", 10))
        combo_mascotas.pack(fill="x", padx=30, pady=5)
        if lista_mascotas_nombres:
            combo_mascotas.current(0)

        tk.Label(ventana_agendar, text="Seleccione Veterinario:", bg="#ffffff", anchor="w").pack(fill="x", padx=30)
        lista_vets_nombres = [v.nombre for v in self.clinica_actual.veterinarios]
        mapa_vets = {v.nombre: v for v in self.clinica_actual.veterinarios}

        combo_vets = ttk.Combobox(ventana_agendar, values=lista_vets_nombres, state="readonly", font=("Helvetica", 10))
        combo_vets.pack(fill="x", padx=30, pady=5)
        if lista_vets_nombres:
            combo_vets.current(0)

        def ejecutar_agendamiento():
            codigo = entry_codigo.get()
            fecha = entry_fecha.get()
            hora = entry_hora.get()
            
            sel_mascota_texto = combo_mascotas.get()
            sel_vet_nombre = combo_vets.get()

            if not sel_mascota_texto or not sel_vet_nombre:
                messagebox.showerror("Error", "Debe seleccionar mascota y veterinario.")
                return

            mascota_obj = mapa_mascotas[sel_mascota_texto]
            vet_obj = mapa_vets[sel_vet_nombre]

            nueva_cita = Cita(codigo, fecha, hora, mascota_obj, vet_obj)

            try:
                self.cita_service.programar_cita(self.clinica_actual.nit, nueva_cita)
                messagebox.showinfo("Éxito", f"¡Cita {codigo} programada correctamente a las {hora}!")
                ventana_agendar.destroy()
            except ValueError as e:
                messagebox.showerror("Conflicto de Horario / Regla de Negocio", str(e))

        tk.Button(ventana_agendar, text="Guardar y Programar Cita", bg="#1b4f8a", fg="white", font=("Helvetica", 10, "bold"), command=ejecutar_agendamiento).pack(pady=20)

    def vista_cancelar_cita(self):
        ventana_cancelar = tk.Toplevel(self.root)
        ventana_cancelar.title("Cancelar Cita")
        ventana_cancelar.geometry("520x280")
        ventana_cancelar.config(bg="#ffffff")

        tk.Label(ventana_cancelar, text="❌ Seleccione la Cita a Cancelar:", bg="#ffffff", font=("Helvetica", 11, "bold")).pack(pady=15)

        citas_programadas = [c for c in self.clinica_actual.citas if c.estado == "Programada"]
        
        lista_citas_texto = []
        mapa_citas = {}
        for c in citas_programadas:
            texto = f"{c.codigo} - {c.mascota.nombre} (Dr. {c.veterinario.nombre}) - {c.fecha} [{c.hora} Hrs]"
            lista_citas_texto.append(texto)
            mapa_citas[texto] = c.codigo

        if not lista_citas_texto:
            messagebox.showinfo("Información", "No hay citas programadas actualmente.")
            ventana_cancelar.destroy()
            return

        combo_citas = ttk.Combobox(ventana_cancelar, values=lista_citas_texto, state="readonly", font=("Helvetica", 10), width=65)
        combo_citas.pack(padx=20, pady=5)
        combo_citas.current(0)

        def ejecutar_cancelacion():
            seleccion = combo_citas.get()
            if not seleccion:
                messagebox.showerror("Error", "Debe seleccionar una cita.")
                return
            codigo = mapa_citas[seleccion]
            try:
                self.cita_service.cancelar_cita(self.clinica_actual.nit, codigo)
                messagebox.showinfo("Éxito", f"¡Cita {codigo} cancelada correctamente!")
                ventana_cancelar.destroy()
            except ValueError as e:
                messagebox.showerror("Error de Regla de Negocio", str(e))

        tk.Button(ventana_cancelar, text="Procesar Cancelación", bg="#d9534f", fg="white", font=("Helvetica", 10, "bold"), command=ejecutar_cancelacion).pack(pady=20)

    def vista_atender_cita(self):
        ventana_atender = tk.Toplevel(self.root)
        ventana_atender.title("Atender Cita y Facturar")
        ventana_atender.geometry("540x460")
        ventana_atender.config(bg="#ffffff")

        tk.Label(ventana_atender, text="🩺 Seleccione la Cita a Atender:", bg="#ffffff", font=("Helvetica", 11, "bold")).pack(pady=10)

        citas_programadas = [c for c in self.clinica_actual.citas if c.estado == "Programada"]
        
        lista_citas_texto = []
        mapa_citas = {}
        for c in citas_programadas:
            texto = f"{c.codigo} - {c.mascota.nombre} (Dr. {c.veterinario.nombre}) - {c.fecha} [{c.hora} Hrs]"
            lista_citas_texto.append(texto)
            mapa_citas[texto] = c.codigo

        if not lista_citas_texto:
            messagebox.showinfo("Información", "No hay citas programadas disponibles para atender.")
            ventana_atender.destroy()
            return

        combo_citas = ttk.Combobox(ventana_atender, values=lista_citas_texto, state="readonly", font=("Helvetica", 10), width=65)
        combo_citas.pack(padx=20, pady=5)
        combo_citas.current(0)

        tk.Label(ventana_atender, text="Seleccione Servicios y Procedimientos Extras:", bg="#ffffff", font=("Helvetica", 10, "bold")).pack(pady=(15, 5))
        
        frame_servicios = tk.Frame(ventana_atender, bg="#ffffff")
        frame_servicios.path = frame_servicios.pack(padx=20, pady=5, fill="x")

        vars_servicios = {}
        for serv in self.clinica_actual.servicios:
            var = tk.IntVar()
            chk = tk.Checkbutton(frame_servicios, text=f"{serv.nombre} ($ {serv.tarifa:,.0f})", variable=var, bg="#ffffff", anchor="w")
            chk.pack(fill="x", anchor="w", pady=2)
            vars_servicios[serv.codigo] = (var, serv)

        def ejecutar_atencion():
            seleccion = combo_citas.get()
            if not seleccion:
                messagebox.showerror("Error", "Debe seleccionar una cita.")
                return
            codigo = mapa_citas[seleccion]

            servicios_extra = []
            for codigo_serv, (var, serv_obj) in vars_servicios.items():
                if var.get() == 1:
                    servicios_extra.append(serv_obj)

            try:
                num_fact = f"FAC-{len(self.clinica_actual.citas):03d}"
                factura = self.cita_service.atender_cita(self.clinica_actual.nit, codigo, servicios_extra, num_fact)
                
                detalle_texto = f"📄 Factura: {factura.numero}\n📅 Fecha: {factura.fecha_emision}\n\nDetalle de Servicios:\n"
                for serv in factura.detalle_servicios:
                    detalle_texto += f" • {serv.nombre}: $ {serv.tarifa:,.0f}\n"
                detalle_texto += f"\n💰 VALOR TOTAL A PAGAR: $ {factura.valor_total:,.0f}"

                messagebox.showinfo("Factura Generada con Éxito", detalle_texto)
                ventana_atender.destroy()
            except ValueError as e:
                messagebox.showerror("Error de Regla de Negocio", str(e))

        tk.Button(ventana_atender, text="Generar Factura y Atender", bg="#2b579a", fg="white", font=("Helvetica", 10, "bold"), command=ejecutar_atencion).pack(pady=20)