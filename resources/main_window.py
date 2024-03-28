from PyQt5.QtWidgets import QMainWindow, QMessageBox
# from PyQt5 import uic
from PyQt5.uic import loadUi

from math import pi, sqrt, log, ceil

from .dict import es, en, warnings
from .data import Data
from .widget_for_table import Table1, Table2

class MainWindow(QMainWindow):
    def __init__(self): # presentation
        # self.__presentador = presentador
        QMainWindow.__init__(self)
        loadUi("resources/views/ui/main.ui", self)

        self.setWindowTitle('Software Helical Coil')
        # self.setWindowIcon(QIcon('./recursos/vistas/assets/logoSS.png'))

        # ZERO PAGE
        # background-color: transparent; ???
        self.label_0_pic_0.setStyleSheet("""
        border-image:url('./resources/views/assets/helical_coil_0.jpg');
        """)
        self.label_0_pic_1.setStyleSheet("""
        border-image:url('./resources/views/assets/logo_univ.svg');
        """)
        self.label_0_pic_2.setStyleSheet("""
        border-image:url('./resources/views/assets/helical_coil_1.jpg');
        """)

        # FUNCTIONAL
        self.pushButton_exit.clicked.connect(self.close)

        button_es = getattr(self, "pushButton_es")
        button_en = getattr(self, "pushButton_en")
        button_es.clicked.connect(lambda _, lang="es": self.set_lang(lang))
        button_en.clicked.connect(lambda _, lang="en": self.set_lang(lang))

        # all pages except zero
        next_buttons = []
        for i in range(1, 8):
            button_next_name = f"pushButton_next_{i}"
            button_next = getattr(self, button_next_name)
            button_prev_name = f"pushButton_previous_{i}"
            button_prev = getattr(self, button_prev_name)
            button_next.clicked.connect(lambda _, page_index=i: self.goto_next_widget(page_index))
            button_prev.clicked.connect(lambda _, page_index=i: self.goto_previous_widget(page_index))
            next_buttons.append(button_next)

        button_prev_name = f"pushButton_previous_{i+1}"
        button_prev = getattr(self, button_prev_name)
        button_prev.clicked.connect(lambda _, page_index=i: self.goto_previous_widget(page_index))

        # THIRD PAGE
        self.wrong_style = """background-color: rgb(255, 62, 62);border: 1px solid black;}QLineEdit:hover{background-color:rgb(229, 0, 0);"""
        self.correct_style = """background-color: rgb(0, 255, 0);border: 1px solid black;}QLineEdit:hover{background-color:rgb(0, 170, 0);"""
        self.standard_style = """background-color: rgb(255, 255, 0);border: 1px solid black;}QLineEdit:hover{background-color:rgb(255, 204, 0);"""

        self.hot_coil = False
        self.hot_shell = True
    
        # FOURTH PAGE
        self.table_1 = Table1()
        self.pushButton0_table_1.clicked.connect(self.show_table_1)
        self.pushButton1_table_1.clicked.connect(self.show_table_1)

        self.table_2 = Table2()
        self.pushButton0_table_2.clicked.connect(self.show_table_2)

        self.lineEdit_hot_Inlet_temperature.textChanged.connect(lambda _, line_edit1=self.lineEdit_hot_Inlet_temperature, line_edit2=self.lineEdit_hot_Outlet_temperature, label=self.label_hot_Average_temperature: self.calculate_mean(line_edit1, line_edit2, label))
        self.lineEdit_hot_Outlet_temperature.textChanged.connect(lambda _, line_edit1=self.lineEdit_hot_Inlet_temperature, line_edit2=self.lineEdit_hot_Outlet_temperature, label=self.label_hot_Average_temperature: self.calculate_mean(line_edit1, line_edit2, label))

        self.lineEdit_cold_Inlet_temperature.textChanged.connect(lambda _, line_edit1=self.lineEdit_cold_Inlet_temperature, line_edit2=self.lineEdit_cold_Outlet_temperature, label=self.label_cold_Average_temperature: self.calculate_mean(line_edit1, line_edit2, label))
        self.lineEdit_cold_Outlet_temperature.textChanged.connect(lambda _, line_edit1=self.lineEdit_cold_Inlet_temperature, line_edit2=self.lineEdit_cold_Outlet_temperature, label=self.label_cold_Average_temperature: self.calculate_mean(line_edit1, line_edit2, label))

        # LAST PAGE
        self.pushButton_restart.clicked.connect(self.reset)

    def reset(self):
        page3 = [self.lineEdit_Name_hot_fluid, self.lineEdit_Name_cold_fluid]
        page4 = [self.label_hot_Average_temperature, self.label_cold_Average_temperature, self.lineEdit_hot_Mass_flowrate, self.lineEdit_hot_Inlet_temperature, self.lineEdit_hot_Outlet_temperature, self.lineEdit_hot_Fouling_factor, self.lineEdit_hot_Allowable_pressure_drop, self.lineEdit_hot_Density, self.lineEdit_hot_Viscosity, self.lineEdit_hot_Specific_heat, self.lineEdit_hot_Thermal_conductivity, self.lineEdit_cold_Mass_flowrate, self.lineEdit_cold_Inlet_temperature, self.lineEdit_cold_Outlet_temperature, self.lineEdit_cold_Fouling_factor, self.lineEdit_cold_Allowable_pressure_drop, self.lineEdit_cold_Density, self.lineEdit_cold_Viscosity, self.lineEdit_cold_Specific_heat, self.lineEdit_cold_Thermal_conductivity]
        page5 = [self.lineEdit_Shell_inner_diameter, self.lineEdit_Core_tube_outer_diameter, self.lineEdit_Average_spiral_diameter, self.lineEdit_Tube_outer_diameter, self.lineEdit_Tube_inner_diameter, self.lineEdit_Tube_pitch, self.lineEdit_Thermal_conductivity_coil_material]
        page6 = [self.label_coil_Heat_load, self.label_shell_Heat_load, self.label_Average_heat_load, self.label_coil_Cross_sectional_area, self.label_coil_Volumetric_flowrate, self.label_coil_Velocity, self.label_coil_Reynolds_number, self.label_coil_Prandtl_number, self.label_coil_Nusselt_number, self.label_coil_Heat_transfer_coefficient, self.label_coil_Heat_transfer_coeficient_inside, self.label_coil_Heat_transfer_coeficient_outside, self.label_Outer_spiral_diameter, self.label_Inner_spiral_diameter, self.label_shell_flow_cross_section, self.label_shell_Volumetric_flowrate, self.label_shell_Velocity, self.label_length_coil_needed, self.label_Volume_shell, self.label_Volume_available_flow_in_shell, self.label_Equivalent_diameter, self.label_shell_Reynolds_number, self.label_shell_Prandtl_number, self.label_shell_Heat_transfer_coeficient]
        page7 = [self.label_Coil_wall_thickness, self.label_Overall_heat_transfer_coeficient, self.label_Log_mean_temperature_difference, self.label_Effective_mean_temperature_difference, self.label_Spiral_total_surface_area, self.label_Numbers_turns_coil, self.label_Height_of_cylinder]
        page8 = [self.label_coil_Factor_E, self.label_coil_Friction_factor, self.label_coil_Pressure_drop, self.label_shell_Drag_coeficient, self.label_shell_Pressure_drop, self.label_coil_Pumping_power, self.label_shell_Pumping_power]
        pages_to_reset = [page3, page4, page5, page6, page7, page8]
        # not_standard_style = [self.label_hot_Average_temperature, self.label_cold_Average_temperature, self.label_4_hot_name, self.label_4_cold_name]
        # blue_color = [self.label_Spiral_total_surface_area, self.label_Numbers_turns_coil, self.label_Calculated_spiral_tube_length, self.label_Height_of_cylinder, self.label_coil_Pressure_drop, self.label_shell_Pressure_drop, self.label_coil_Pumping_power, self.label_shell_Pumping_power]

        i = 0
        for page in pages_to_reset:
            for item in page:
                item.setText("")
                if i < 3:
                    item.setStyleSheet(self.standard_style)
                # and item not in not_standard_style + blue_color
                # elif item in blue_color:
                #     item.setStyleSheet("""background-color:rgb(0, 85, 255);""")
            i += 1

        self.label_ratio_Qh_Qc.setStyleSheet("""background-color: rgb(25, 17, 255);""")

        # FOR SOME REASON NONE OF THE TWO APPROACHES WORK
        selected = self.buttonGroup.checkedButton()
        selected.setChecked(False)
        self.radioButton_coil.setChecked(False)
        self.radioButton_shell.setChecked(False)
        
        self.stackedWidget.setCurrentIndex(0)

    def show_table_1(self):
        # for creating a new table every time the button is clicked
        if self.table_1:
            self.table_1 = Table1(self.lang)
            self.table_1.show()

    def show_table_2(self):
        # for creating a new table every time the button is clicked
        if self.table_2:
            self.table_2 = Table2(self.lang)
            self.table_2.show()

    def calculate_mean(self, line_edit1, line_edit2, label):
        try:
            hot_in = float(line_edit1.text().replace(",", "."))
            hot_out = float(line_edit2.text().replace(",", "."))
        except ValueError as e:
            print(e)
        except Exception as unecpected_err:
            print(unecpected_err)
        else:
            mean = (hot_in + hot_out) / 2
            label.setText(str(mean))

    def set_lang(self, lang):
        self.lang = lang
        if lang == "es":
            for k in es.keys():
                item = getattr(self, k)
                item.setText(es[k])
            
            if self.hot_shell:
                shell = "caliente"
                coil = "frío"
            elif self.hot_coil:
                shell = "frío"
                coil = "caliente"
            item = getattr(self, "label_6_1_coil")
            item.setText("Fluido {0} (serpentín)".format(coil))
            item = getattr(self, "label_6_3_shell")
            item.setText("Fluido {0} (coraza)".format(shell))

            item = getattr(self, "label_6_2_coil")
            item.setText("Carga de calor (Q{0})".format("c" if coil=="frío" else "h"))
            item = getattr(self, "label_6_4_shell")
            item.setText("Carga de calor (Q{0})".format("c" if shell=="frío" else "h"))

            item = getattr(self, "label_8_1_coil")
            item.setText("Fluido {0} (serpentín)".format(coil))
            item = getattr(self, "label_8_5_shell")
            item.setText("Fluido {0} (coraza)".format(shell))

            item = getattr(self, "label_8_9_coil")
            item.setText("Fluido {0} (serpentín)".format(coil))
            item = getattr(self, "label_8_12_shell")
            item.setText("Fluido {0} (coraza)".format(shell))
        
        elif lang == "en":
            for k in en.keys():
                item = getattr(self, k)
                item.setText(en[k])

            if self.hot_shell:
                shell = "Hot"
                coil = "Cold"
            elif self.hot_coil:
                shell = "Cold"
                coil = "Hot"
            item = getattr(self, "label_6_1_coil")
            item.setText("{0} fluid (serpentín)".format(coil))
            item = getattr(self, "label_6_3_shell")
            item.setText("{0} fluid (coraza)".format(shell))

            item = getattr(self, "label_6_2_coil")
            item.setText("Heat load (Q{0})".format("c" if coil=="Cold" else "h"))
            item = getattr(self, "label_6_4_shell")
            item.setText("Heat load (Q{0})".format("c" if shell=="Cold" else "h"))

            item = getattr(self, "label_8_1_coil")
            item.setText("{0} fluid (serpentín)".format(coil))
            item = getattr(self, "label_8_5_shell")
            item.setText("{0} fluid (coraza)".format(shell))

            item = getattr(self, "label_8_9_coil")
            item.setText("{0} fluid (serpentín)".format(coil))
            item = getattr(self, "label_8_12_shell")
            item.setText("{0} fluid (coraza)".format(shell))
        self.goto_next_widget(0) # go to the page number one

    def goto_next_widget(self, page_index):
        if page_index == 3:
            if not self.check_page_3_data():
                return
        elif page_index == 4:
            if not self.check_page_4_data():
                return
        elif page_index == 5:
            if not self.check_page_5_data():
                return
            else:
                self.load_results()
        self.stackedWidget.setCurrentIndex(page_index + 1)

    def goto_previous_widget(self, page_index):
       self.stackedWidget.setCurrentIndex(page_index - 1)

    def check_page_3_data(self):
        if not self.fluids_names_entered():
            return False
        if not self.radioButton_selected():
            return False
        self.store_page_3_data()
        return True

    def fluids_names_entered(self):
        self.hot_name = self.lineEdit_Name_hot_fluid.text()
        self.cold_name = self.lineEdit_Name_cold_fluid.text()
        if not self.hot_name:
            # object_name = self.lineEdit_Name_hot_fluid.objectName()
            self.lineEdit_Name_hot_fluid.setStyleSheet(self.wrong_style)
            self.warn_one_line_edit(self.lineEdit_Name_hot_fluid.objectName(), "EmptyLineError")
            return False
        self.lineEdit_Name_hot_fluid.setStyleSheet(self.correct_style)
        if not self.cold_name:
            # object_name = self.lineEdit_Name_cold_fluid.objectName()
            self.lineEdit_Name_cold_fluid.setStyleSheet(self.wrong_style)
            self.warn_one_line_edit(self.lineEdit_Name_cold_fluid.objectName(), "EmptyLineError")
            return False
        self.lineEdit_Name_cold_fluid.setStyleSheet(self.correct_style)
        return True
    
    def radioButton_selected(self):
        selected = self.buttonGroup.checkedButton()
        if not selected:
            # object_name = self.lineEdit_Name_hot_fluid.objectName()
            self.warn_one_line_edit(self.lineEdit_Name_hot_fluid.objectName(), "SelectionError")
            return False
        
        text = selected.text()
        if text == "Shell":
            self.hot_shell = True
            self.cold_shell = False
        elif text == "Coil":
            self.hot_shell = False
            self.cold_shell = True
        return True
    def store_page_3_data(self):
        self.label_4_hot_name.setText(self.hot_name)
        self.label_4_cold_name.setText(self.cold_name)

    def check_page_4_data(self):
        # check if there's any empty line in any of the above widgets and warn about it
        self.line_edits_4 = [self.lineEdit_hot_Mass_flowrate, self.lineEdit_hot_Inlet_temperature, self.lineEdit_hot_Outlet_temperature, self.lineEdit_hot_Fouling_factor, self.lineEdit_hot_Allowable_pressure_drop, self.lineEdit_hot_Density, self.lineEdit_hot_Viscosity, self.lineEdit_hot_Specific_heat, self.lineEdit_hot_Thermal_conductivity, self.lineEdit_cold_Mass_flowrate, self.lineEdit_cold_Inlet_temperature, self.lineEdit_cold_Outlet_temperature, self.lineEdit_cold_Fouling_factor, self.lineEdit_cold_Allowable_pressure_drop, self.lineEdit_cold_Density, self.lineEdit_cold_Viscosity, self.lineEdit_cold_Specific_heat, self.lineEdit_cold_Thermal_conductivity]

        if not self.check_page_data(self.line_edits_4):
            return False
    
        self.hot_Mass_flowrate = Data()
        self.hot_Inlet_temperature = Data()
        self.hot_Outlet_temperature = Data()
        self.hot_Fouling_factor = Data()
        self.hot_Allowable_pressure_drop = Data()
        self.hot_Density = Data()
        self.hot_Viscosity = Data()
        self.hot_Specific_heat = Data()
        self.hot_Thermal_conductivity = Data()
        self.cold_Mass_flowrate = Data()
        self.cold_Inlet_temperature = Data()
        self.cold_Outlet_temperature = Data()
        self.cold_Fouling_factor = Data()
        self.cold_Allowable_pressure_drop = Data()
        self.cold_Density = Data()
        self.cold_Viscosity = Data()
        self.cold_Specific_heat = Data()
        self.cold_Thermal_conductivity = Data()
        
        self.data_objects_4 = [self.hot_Mass_flowrate, self.hot_Inlet_temperature, self.hot_Outlet_temperature, self.hot_Fouling_factor, self.hot_Allowable_pressure_drop, self.hot_Density, self.hot_Viscosity, self.hot_Specific_heat, self.hot_Thermal_conductivity, self.cold_Mass_flowrate, self.cold_Inlet_temperature, self.cold_Outlet_temperature, self.cold_Fouling_factor, self.cold_Allowable_pressure_drop, self.cold_Density, self.cold_Viscosity, self.cold_Specific_heat, self.cold_Thermal_conductivity]
        if not self.convert_and_store_data(self.data_objects_4, self.line_edits_4):
            return False

        self.label_hot_Average_temperature.setText(str((self.hot_Inlet_temperature.data + self.hot_Outlet_temperature.data) / 2))
        self.label_cold_Average_temperature.setText(str((self.cold_Inlet_temperature.data + self.cold_Outlet_temperature.data) / 2))
        return True

    def check_page_data(self, line_edits):
        count = 0
        empties = []
        for line_edit in line_edits:
            if not line_edit.text():
                count += 1
                empties.append(line_edit)
                # line_edit.setStyleSheet(self.wrong_style)
            # else:
            #     line_edit.setStyleSheet(self.standard_style)
            
        if count:
            if count == 1:
                self.warn_one_line_edit(line_edit.objectName(), "EmptyLineError")
            else:
                names = [line_edit.objectName() for line_edit in empties]
                self.warn_serveral_line_edits(names, "SeveralEmptyLinesError")
            return False
        # warn_serveral_line_edits
        return True

    def convert_and_store_data(self, data_objects, line_edits):
        not_converted = []
        errors = []
        for i in range(len(data_objects)):
            try:
                data_objects[i].data = float(line_edits[i].text().replace(",", "."))
            except ValueError as e:
                line_edits[i].setStyleSheet(self.wrong_style)
                print(e)
                # show in the console the error
                errors.append(e)
                
                # store the ones that couldn't be converted
                not_converted.append(line_edits[i])
                line_edits[i].setStyleSheet(self.wrong_style)
                continue
            # except Exception as err:
            #     print(f"Unexpected {err=}, {type(err)=}")
            #     return False
            else:
                line_edits[i].setStyleSheet(self.correct_style)

        if errors:
            if len(errors) == 1:
                object_name = line_edits[i].objectName()
                err_list = str(errors[0]).split(" ")
                invalid_data = err_list[len(err_list) - 1]
                self.warn_one_line_edit(object_name, "ValueError", invalid_data)
            else:
                invalid_datas = []
                for e in errors:
                    err_list = str(e).split(" ")
                    invalid_data = err_list[len(err_list) - 1]
                    invalid_datas.append(invalid_data)
                object_names = [line_edit.objectName() for line_edit in not_converted]
                self.warn_serveral_line_edits(object_names, "SeveralValuesError", invalid_datas)
            return False
        return True

    def check_page_5_data(self):
        self.line_edits_5 = [self.lineEdit_Shell_inner_diameter, self.lineEdit_Core_tube_outer_diameter, self.lineEdit_Average_spiral_diameter, self.lineEdit_Tube_outer_diameter, self.lineEdit_Tube_inner_diameter, self.lineEdit_Tube_pitch, self.lineEdit_Thermal_conductivity_coil_material]
        
        if not self.check_page_data(self.line_edits_5):
            return False
        # for line_edit in self.line_edits_5:
        #     if not line_edit.text():
        #         # object_name = line_edit.objectName()
        #         line_edit.setStyleSheet(self.wrong_style)
        #         self.warn_one_line_edit(line_edit.objectName(), "EmptyLineError")
        #         return False
        #     else:
        #         line_edit.setStyleSheet(self.standard_style)

        self.Shell_inner_diameter = Data()
        self.Core_tube_outer_diameter = Data()
        self.Average_spiral_diameter = Data()
        self.Tube_outer_diameter = Data()
        self.Tube_inner_diameter = Data()
        self.Tube_pitch = Data()
        self.Thermal_conductivity_coil_material = Data()
        self.data_objects_5 = [self.Shell_inner_diameter, self.Core_tube_outer_diameter, self.Average_spiral_diameter, self.Tube_outer_diameter, self.Tube_inner_diameter, self.Tube_pitch, self.Thermal_conductivity_coil_material]

        if not self.convert_and_store_data(self.data_objects_5, self.line_edits_5):
            return False
        return True

    # calculate the results for pages 6, 7 and 8
    def load_results(self):
        # print("rectification")
        # print(self.data_objects_5[0] is self.Shell_inner_diameter)
        # print(self.data_objects_5[1] is self.Core_tube_outer_diameter)
        # print(self.data_objects_5[2] is self.Average_spiral_diameter)
        # print(self.data_objects_5[3] is self.Tube_outer_diameter)
        # print(self.data_objects_5[4] is self.Tube_inner_diameter)
        # print("end rectification")

        Qh = (self.hot_Mass_flowrate.data * self.hot_Specific_heat.data * (self.hot_Inlet_temperature.data - self.hot_Outlet_temperature.data)) / 3600
        Qc = (self.cold_Mass_flowrate.data * self.cold_Specific_heat.data * (self.cold_Outlet_temperature.data - self.cold_Inlet_temperature.data)) / 3600
        try:
            ratio = Qh / Qc
        except ZeroDivisionError as e:
            print(f"{e}\nRatio isn't correct. Please, check the related parameters in the previous pages (red colored).")
            ratio = warnings["ZeroDivisionError"][self.lang]
            self.label_ratio_Qh_Qc.setText(ratio)
            self.warn_wrong_ratio("RatioError")
            return
        else:
            if not 1.030 > ratio > 0.970:
                self.label_ratio_Qh_Qc.setText(str(round(ratio, 3)))
                self.warn_wrong_ratio("RatioError")
                return
        self.label_ratio_Qh_Qc.setText(str(round(ratio, 3)))
        self.label_ratio_Qh_Qc.setStyleSheet(self.correct_style)
        Qe = (Qh + Qc) / 2

        if self.hot_shell:
            coil_Mass_flowrate = self.cold_Mass_flowrate.data
            coil_Density = self.cold_Density.data
            coil_Viscosity = self.cold_Viscosity.data
            coil_Specific_heat = self.cold_Specific_heat.data
            coil_Thermal_conductivity = self.cold_Thermal_conductivity.data
            coil_Fouling_factor = self.cold_Fouling_factor.data
            # coil_Outlet_temperature = self.cold_Outlet_temperature
            # coil_Inlet_temperature = self.cold_Inlet_temperature
            coil_heat_load = Qc

            shell_Mass_flowrate = self.hot_Mass_flowrate.data
            shell_Density = self.hot_Density.data
            shell_Viscosity = self.hot_Viscosity.data
            shell_Specific_heat = self.hot_Specific_heat.data
            shell_Thermal_conductivity = self.hot_Thermal_conductivity.data
            shell_Fouling_factor = self.hot_Fouling_factor.data
            # shell_Inlet_temperature = self.hot_Inlet_temperature
            # shell_Outlet_temperature = self.hot_Outlet_temperature
            shell_heat_load = Qh

        elif self.hot_coil:
            shell_Mass_flowrate = self.cold_Mass_flowrate.data
            shell_Density = self.cold_Density.data
            shell_Viscosity = self.cold_Viscosity.data
            shell_Specific_heat = self.cold_Specific_heat.data
            shell_Thermal_conductivity = self.cold_Thermal_conductivity.data
            shell_Fouling_factor = self.cold_Fouling_factor.data
            # shell_Outlet_temperature = self.cold_Outlet_temperature
            # shell_Inlet_temperature = self.cold_Inlet_temperature
            shell_heat_load = Qc

            coil_Mass_flowrate = self.hot_Mass_flowrate.data
            coil_Density = self.hot_Density.data
            coil_Viscosity = self.hot_Viscosity.data
            coil_Specific_heat = self.hot_Specific_heat.data
            coil_Thermal_conductivity = self.hot_Thermal_conductivity.data
            coil_Fouling_factor = self.hot_Fouling_factor.data
            # coil_Inlet_temperature = self.hot_Inlet_temperature
            # coil_Outlet_temperature = self.hot_Outlet_temperature
            coil_heat_load = Qh

        Average_spiral_diameter = self.Average_spiral_diameter.data
        Tube_inner_diameter = self.Tube_inner_diameter.data
        Tube_outer_diameter = self.Tube_outer_diameter.data

        Shell_inner_diameter = self.Shell_inner_diameter.data
        Core_tube_outer_diameter = self.Core_tube_outer_diameter.data
        Tube_pitch = self.Tube_pitch.data
        Thermal_conductivity_coil_material = self.Thermal_conductivity_coil_material.data
    
    # calculations of the page 6
        cross_sectional_coil_area = (pi * Tube_inner_diameter ** 2) / 4
        coil_volumetric_flowrate = coil_Mass_flowrate / coil_Density / 3600
        coil_velocity = coil_volumetric_flowrate / cross_sectional_coil_area
        coil_Reynolds_number = (Tube_inner_diameter * coil_velocity * coil_Density) / coil_Viscosity
        coil_Prandtl_number = ((coil_Specific_heat * coil_Viscosity) / coil_Thermal_conductivity) * 1000
        if coil_Reynolds_number > 8000:
            coil_Nusselt_number = 0.023 * (coil_Reynolds_number ** 0.8) * (coil_Prandtl_number ** 0.33)
            coil_heat_transfer_coeficient = coil_Nusselt_number * coil_Thermal_conductivity / Tube_inner_diameter
            coil_heat_transfer_coeficient_inside_diameter = coil_heat_transfer_coeficient * (1 + 3.5 * Tube_inner_diameter / Average_spiral_diameter)
            coil_heat_transfer_coeficient_outside_diameter = coil_heat_transfer_coeficient_inside_diameter * Tube_inner_diameter / Tube_outer_diameter
        
        outer_spiral_diameter = Shell_inner_diameter - Tube_outer_diameter
        inner_spiral_diameter = Core_tube_outer_diameter + Tube_outer_diameter
        shell_flow_cross_section = pi/4 * ((Shell_inner_diameter**2 - Core_tube_outer_diameter**2) - (outer_spiral_diameter**2 - inner_spiral_diameter**2))
        shell_volumetric_flowrate = shell_Mass_flowrate / shell_Density / 3600
        shell_velocity = shell_volumetric_flowrate / shell_flow_cross_section
        length_coil_needed = round(sqrt((pi * Average_spiral_diameter)**2 + Tube_pitch**2), 3)
        volume_occupied_by_coil = pi/4 * (Tube_outer_diameter**2) * length_coil_needed
        volume_of_shell = pi/4 * (Shell_inner_diameter**2 - Core_tube_outer_diameter**2) * Tube_pitch
        volume_available_flow_shell = volume_of_shell - volume_occupied_by_coil
        equivalent_diameter = (4 * volume_available_flow_shell) / (pi * Tube_outer_diameter * length_coil_needed)
        shell_Reynolds_number = (equivalent_diameter * shell_velocity * shell_Density) / shell_Viscosity
        shell_Prandtl_number = ((shell_Specific_heat * shell_Viscosity) / shell_Thermal_conductivity) * 1000
        if 50 < shell_Reynolds_number < 10000:
            shell_heat_transfer_coeficient = 0.6 * (shell_Thermal_conductivity / equivalent_diameter) * (shell_Reynolds_number**0.5) * (shell_Prandtl_number**0.31)
        elif shell_Prandtl_number >= 10000:
            shell_heat_transfer_coeficient = 0.36 * (shell_Thermal_conductivity / equivalent_diameter) * (shell_Reynolds_number**0.55) * (shell_Prandtl_number**0.33)

    # set the results in their labels
        self.label_coil_Heat_load.setText(str(round(coil_heat_load, 2)))
        self.label_shell_Heat_load.setText(str(round(shell_heat_load, 2))) #  expected: 36.97 ,  real: 36.96
        self.label_Average_heat_load.setText(str(round(Qe, 2))) #  expected: 36.77 ,  real: 36.76

        self.label_coil_Cross_sectional_area.setText(str(round(cross_sectional_coil_area, 5)))
        self.label_coil_Volumetric_flowrate.setText(str(round(coil_volumetric_flowrate, 6)))
        self.label_coil_Velocity.setText(str(round(coil_velocity, 3))) # 
        self.label_coil_Reynolds_number.setText(str(round(coil_Reynolds_number, 2))) #  expected: 11188.45,  real: 11182.78
        self.label_coil_Prandtl_number.setText(str(round(coil_Prandtl_number, 2))) 
        if coil_Reynolds_number > 8000:
            self.label_coil_Nusselt_number.setText(str(round(coil_Nusselt_number, 2))) #  expected: 69.64,  real: 69.61
            self.label_coil_Heat_transfer_coefficient.setText(str(round(coil_heat_transfer_coeficient, 2))) #  expected: 1713.11,  real: 1712.42
            self.label_coil_Heat_transfer_coeficient_inside.setText(str(round(coil_heat_transfer_coeficient_inside_diameter, 2))) #  expected: 2087.85,  real: 2087.01
            self.label_coil_Heat_transfer_coeficient_outside.setText(str(round(coil_heat_transfer_coeficient_outside_diameter, 2))) #  expected: 1739.88 ,  real: 1739.17
            
        self.label_Outer_spiral_diameter.setText(str(round(outer_spiral_diameter, 3)))
        self.label_Inner_spiral_diameter.setText(str(round(inner_spiral_diameter, 3)))
        self.label_shell_flow_cross_section.setText(str(round(shell_flow_cross_section, 3)))
        self.label_shell_Volumetric_flowrate.setText(str(round(shell_volumetric_flowrate, 4)))
        self.label_shell_Velocity.setText(str(round(shell_velocity, 4)))
        self.label_length_coil_needed.setText(str(length_coil_needed))
        self.label_Volume_occupied_coil.setText(str(round(volume_occupied_by_coil, 4)))
        self.label_Volume_shell.setText(str(round(volume_of_shell, 4)))
        self.label_Volume_available_flow_in_shell.setText(str(round(volume_available_flow_shell, 4)))
        self.label_Equivalent_diameter.setText(str(round(equivalent_diameter, 3)))
        self.label_shell_Reynolds_number.setText(str(round(shell_Reynolds_number, 2))) # expected: 1384.25 , real: 1383.9
        self.label_shell_Prandtl_number.setText(str(round(shell_Prandtl_number, 2))) # exp: 5.26 , real: 5.25
        if shell_Reynolds_number > 50:
            self.label_shell_Heat_transfer_coeficient.setText(str(round(shell_heat_transfer_coeficient, 2)))   # expected: 83.92 , real: 83.94   

    # page 7
        coil_wall_thickness = (Tube_outer_diameter - Tube_inner_diameter) / 2
        overall_heat_transfer_coeficient = 1 / ((1 / coil_heat_transfer_coeficient_outside_diameter) + (1 / shell_heat_transfer_coeficient) + (coil_wall_thickness / Thermal_conductivity_coil_material) + shell_Fouling_factor + coil_Fouling_factor)

        # for countercurrent flow 
        hot_Inlet_temperature = self.hot_Inlet_temperature.data
        hot_Outlet_temperature = self.hot_Outlet_temperature.data
        cold_Inlet_temperature = self.cold_Inlet_temperature.data
        cold_Outlet_temperature = self.cold_Outlet_temperature.data

        log_mean_temp_difference = ((hot_Inlet_temperature - cold_Outlet_temperature) - (hot_Outlet_temperature - cold_Inlet_temperature)) / (log((hot_Inlet_temperature - cold_Outlet_temperature) / (hot_Outlet_temperature - cold_Inlet_temperature)))
        effective_mean_temperature_difference = log_mean_temp_difference * 0.99
        spiral_total_surface_area = (Qe / (overall_heat_transfer_coeficient * effective_mean_temperature_difference)) * 1000
        number_of_turns_coil = ceil(spiral_total_surface_area / (pi * Tube_outer_diameter * length_coil_needed))
        calculated_spiral_total_tube_length = length_coil_needed * number_of_turns_coil
        height_of_cylinder = number_of_turns_coil * Tube_pitch + Tube_outer_diameter

    # set the results in their labels
        self.label_Coil_wall_thickness.setText(str(round(coil_wall_thickness, 4)))
        self.label_Overall_heat_transfer_coeficient.setText(str(round(overall_heat_transfer_coeficient, 2))) # expected: 76.69, real: 76.71
        self.label_Log_mean_temperature_difference.setText(str(round(log_mean_temp_difference, 2)))
        self.label_Effective_mean_temperature_difference.setText(str(round(effective_mean_temperature_difference, 2)))
        self.label_Spiral_total_surface_area.setText(str(round(spiral_total_surface_area, 2)))
        self.label_Numbers_turns_coil.setText(str(number_of_turns_coil))
        self.label_Calculated_spiral_tube_length.setText(str(round(calculated_spiral_total_tube_length, 2))) # expected: 173.44 , real: 173.53
        self.label_Height_of_cylinder.setText(str(round(height_of_cylinder, 2)))

    # page 8
        coil_Factor_E = Average_spiral_diameter * (1 + (Tube_pitch / (pi * Average_spiral_diameter)) ** 2)
        coil_Friction_factor = ((0.3164 / (coil_Reynolds_number**0.25) + 0.03*((Tube_inner_diameter / coil_Factor_E)**(1/2)) )) * 1 # (miu_w / miu)**0.27
        coil_Pressure_drop = coil_Friction_factor * (calculated_spiral_total_tube_length/Tube_inner_diameter) * ((coil_velocity**2 * coil_Density)/2)
        
        shell_drag_coeficient = (0.3164 / (shell_Reynolds_number**0.25)) * (1 + 0.095 * ((Tube_outer_diameter/Average_spiral_diameter)**1/2) * (shell_Reynolds_number**0.25))
        shell_Pressure_drop = shell_drag_coeficient * (height_of_cylinder / equivalent_diameter) * ((shell_velocity**2 * shell_Density)/2)
        
        coil_Pumping_power = (coil_Pressure_drop * (coil_Mass_flowrate / 3600)) / (0.8 * coil_Density)
        shell_Pumping_power = (shell_Pressure_drop * (shell_Mass_flowrate / 3600)) / (0.8 * shell_Density)

    # set the results in their labels
        self.label_coil_Factor_E.setText(str(round(coil_Factor_E, 4)))
        self.label_coil_Friction_factor.setText(str(round(coil_Friction_factor, 4)))
        self.label_coil_Pressure_drop.setText(str(round(coil_Pressure_drop, 2)))
        
        self.label_shell_Drag_coeficient.setText(str(round(shell_drag_coeficient, 4)))
        self.label_shell_Pressure_drop.setText(str(round(shell_Pressure_drop, 4)))

        self.label_coil_Pumping_power.setText(str(round(coil_Pumping_power, 2)))
        self.label_shell_Pumping_power.setText(str(round(shell_Pumping_power, 6)))


    def warn_one_line_edit(self, lineEdit_object_name, error_name, invalid_data=None):
        # label_name = " ".join(lineEdit_object_name.split("_")[2:]) # for instance, 'Mass flowrate'
        label_name = "label" + lineEdit_object_name[8:]
        label = getattr(self, label_name)
        label_text = label.text()
        if error_name == "EmptyLineError":
            console_error_text = f"{error_name}: The lineEdit '{lineEdit_object_name}', associated to the label '{label_name}' cannot be empty since it is needed for calculations."
        elif error_name == "SelectionError":
            console_error_text = f"{error_name}: There's no radio button group selected for localizing the hot fluid at page 4."
        elif error_name == "ValueError":
            console_error_text = f"{error_name}: The lineEdit '{lineEdit_object_name}', associated to the label '{label_name}' has a invalid data."
        print(console_error_text)

        if invalid_data:
            label_text = invalid_data
            
        QMessageBox.warning(self, warnings[error_name]["title"][self.lang],
                                warnings[error_name]["text"][self.lang].format(label_text))

    def warn_serveral_line_edits(self, lineEdit_object_names, error_name, invalid_datas=[]):
        label_text = ""
        for line_edit_name in lineEdit_object_names:
            label_name = "label" + line_edit_name[8:]
            label = getattr(self, label_name)
            label_text = label_text + label.text() + ", "
        label_text = label_text[:len(label_text) - 2] # eliminate the last comma and the space
        if error_name == "SeveralEmptyLinesError":
            console_error_text = f"{error_name}: The lineEdits '{lineEdit_object_names}', cannot be empty since they are needed for calculations."
        elif error_name == "SeveralValuesError":
            console_error_text = f"{error_name}: The lineEdits '{lineEdit_object_names}' have invalid datas."
        print(console_error_text)

        if invalid_datas:
            label_text = invalid_datas
            
        QMessageBox.warning(self, warnings[error_name]["title"][self.lang],
                                warnings[error_name]["text"][self.lang].format(label_text))

    def warn_wrong_ratio(self, error_name):
        print("Ratio isn't correct. Please, check the related parameters in the previous pages (red colored).")
        QMessageBox.warning(self, warnings[error_name]["title"][self.lang],
                                warnings[error_name]["text"][self.lang])
        self.label_ratio_Qh_Qc.setStyleSheet(self.wrong_style)
        self.lineEdit_hot_Mass_flowrate.setStyleSheet(self.wrong_style)
        self.lineEdit_hot_Specific_heat.setStyleSheet(self.wrong_style)
        self.lineEdit_hot_Inlet_temperature.setStyleSheet(self.wrong_style)
        self.lineEdit_hot_Outlet_temperature.setStyleSheet(self.wrong_style)

        self.lineEdit_cold_Mass_flowrate.setStyleSheet(self.wrong_style)
        self.lineEdit_cold_Specific_heat.setStyleSheet(self.wrong_style)
        self.lineEdit_cold_Inlet_temperature.setStyleSheet(self.wrong_style)
        self.lineEdit_cold_Outlet_temperature.setStyleSheet(self.wrong_style)